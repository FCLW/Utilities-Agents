#!/usr/bin/env python3
"""
record_agent_demo.py — Authentic Gemini Enterprise Live Agent Demo Video Recorder

Automates end-to-end recording of Gemini Enterprise Agent demo walkthroughs directly
inside the real Google Gemini Enterprise (GE) web application:
1. Browser Automation: Launches Google Chrome with the authenticated user profile (Profile 1)
   at 1920x1080 (1080p).
2. Navigation: Navigates to Gemini Enterprise URL, clicks "Agents" tab in the left sidebar,
   searches for the agent by title, and opens the dedicated agent workspace.
3. Execution: Executes authentic curated business prompts from sample_prompts.yaml
   or README.md, submits via the genuine GE prompt input box, and waits for the live
   streaming response and tool execution (BigQueryQueryTool, etc.) to complete.
4. Smooth Scrolling: Performs smooth mouse scroll walkthrough across the live chat conversation.
5. Video Encoding: Encodes the recorded session into 1080p MP4 via FFmpeg (H.264, CRF 22, yuv420p, faststart).
6. HTML Showcase: Updates the standalone HTML player in demos/<domain>/<agent_name>.html.
7. Cloud Storage: Optionally syncs/uploads all demo assets to gs://utilities-agents-demos/.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.prompt_parser import get_catalog_entry, parse_agent_prompts, resolve_agent_domain
from scripts.generate_demo_html import DOMAIN_ICONS, DOMAIN_TITLES, generate_html_showcase

DEFAULT_GE_URL = os.getenv(
    "GEMINI_ENTERPRISE_URL",
    "https://vertexaisearch.cloud.google.com/home/cid/4d886c3b-e9e0-419c-a168-d25114e2dad6"
)
DEFAULT_SOURCE_CHROME_DIR = Path.home() / ".config" / "google-chrome"
DEFAULT_BASE_RECORDER_DIR = Path.home() / ".config" / "google-chrome-demo-recorder"
DEFAULT_CHROME_PROFILE_DIR = os.getenv("CHROME_PROFILE_DIR", "Profile 1")

RESOLUTION_CONFIGS = {
    "1080p": {"width": 1920, "height": 1080},
    "720p": {"width": 1280, "height": 720},
}


def sync_chrome_profile(target_dir: Path, profile_dir: str = DEFAULT_CHROME_PROFILE_DIR):
    """Syncs user Chrome profile into demo recorder directory to avoid singleton locks."""
    source_dir = DEFAULT_SOURCE_CHROME_DIR
    if source_dir.resolve() == target_dir.resolve():
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Sync Local State
    local_state_src = source_dir / "Local State"
    local_state_tgt = target_dir / "Local State"
    if local_state_src.exists():
        shutil.copy2(local_state_src, local_state_tgt)

    # 2. Rsync the profile directory (Cookies, Storage, Auth state)
    p_src = source_dir / profile_dir
    p_tgt = target_dir / profile_dir
    if p_src.exists():
        p_tgt.mkdir(parents=True, exist_ok=True)
        cmd = [
            "rsync", "-av", "--delete",
            "--exclude=Singleton*",
            "--exclude=*lock*",
            "--exclude=LOCK*",
            "--exclude=*Cache*",
            "--exclude=*Crash*",
            "--exclude=BrowserMetrics*",
            str(p_src) + "/",
            str(p_tgt) + "/"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_video_duration(video_path: Path) -> float:
    """Returns the duration of a video file in seconds using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0


def convert_webm_to_mp4(
    webm_path: Path,
    mp4_path: Path,
    wait_intervals: list[tuple[float, float]] | None = None,
    speedup_factor: float = 6.0
) -> bool:
    """Converts recorded webm video to high-quality universal MP4 using ffmpeg,
    selectively accelerating waiting/streaming intervals by speedup_factor.
    """
    total_duration = get_video_duration(webm_path)

    # If no intervals or invalid duration, standard conversion
    if not wait_intervals or total_duration <= 0 or speedup_factor <= 1.0:
        try:
            print(f"🔄 Converting {webm_path.name} to MP4 format...", flush=True)
            cmd = [
                "ffmpeg", "-y",
                "-i", str(webm_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "22",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                str(mp4_path)
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 0
        except Exception as e:
            print(f"⚠️ FFmpeg conversion error: {e}", flush=True)
            return False

    # Process and sanitize intervals
    sanitized = []
    for s, e in sorted(wait_intervals, key=lambda x: x[0]):
        s_clamped = max(0.0, min(s, total_duration))
        e_clamped = max(0.0, min(e, total_duration))
        if e_clamped - s_clamped >= 1.0:
            sanitized.append((s_clamped, e_clamped))

    # Merge overlapping intervals
    merged = []
    for s, e in sanitized:
        if not merged:
            merged.append([s, e])
        else:
            prev_s, prev_e = merged[-1]
            if s <= prev_e:
                merged[-1][1] = max(prev_e, e)
            else:
                merged.append([s, e])

    # Build segments across [0, total_duration]
    segments = []  # list of (start, end, is_speedup)
    cur = 0.0
    for s, e in merged:
        if s > cur + 0.1:
            segments.append((cur, s, False))
        segments.append((s, e, True))
        cur = e
    if cur + 0.1 < total_duration:
        segments.append((cur, total_duration, False))

    if not segments:
        segments = [(0.0, total_duration, False)]

    # Build filtergraph
    filter_parts = []
    stream_labels = []
    for idx, (seg_s, seg_e, is_speed) in enumerate(segments):
        label = f"v{idx}"
        pts_expr = f"(PTS-STARTPTS)/{speedup_factor:.1f}" if is_speed else "PTS-STARTPTS"
        filter_parts.append(
            f"[0:v]trim=start={seg_s:.2f}:end={seg_e:.2f},setpts={pts_expr}[{label}]"
        )
        stream_labels.append(f"[{label}]")

    concat_part = f"{''.join(stream_labels)}concat=n={len(stream_labels)}:v=1:a=0[outv]"
    full_filter = f"{';'.join(filter_parts)};{concat_part}"

    try:
        speed_msg = f" (accelerating {len(merged)} waiting intervals {speedup_factor:.1f}x)"
        print(f"🔄 Converting & accelerating {webm_path.name} to MP4{speed_msg}...", flush=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(webm_path),
            "-filter_complex", full_filter,
            "-map", "[outv]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(mp4_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            return True
        else:
            print(f"⚠️ FFmpeg filtergraph returned non-zero, falling back to standard encoding...", flush=True)
    except Exception as e:
        print(f"⚠️ FFmpeg acceleration error: {e}, falling back...", flush=True)

    # Graceful fallback to standard conversion
    try:
        cmd_fallback = [
            "ffmpeg", "-y",
            "-i", str(webm_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(mp4_path)
        ]
        res_fb = subprocess.run(cmd_fallback, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res_fb.returncode == 0
    except Exception as fb_err:
        print(f"❌ Fallback conversion failed: {fb_err}", flush=True)
        return False


async def record_single_agent(
    agent_name: str,
    domain: str,
    output_dir: Path,
    ge_url: str = DEFAULT_GE_URL,
    profile_dir: str = DEFAULT_CHROME_PROFILE_DIR,
    recorder_base_dir: Path = DEFAULT_BASE_RECORDER_DIR,
    worker_id: int = 0,
    headless: bool = True,
    turns_count: int = 4,
    typing_delay: int = 35,
    read_pause: float = 2.2,
    speedup_factor: float = 10.0,
    skip_existing: bool = False,
    upload: bool = False
) -> Path | None:
    from playwright.async_api import async_playwright

    domain_output_dir = output_dir / domain
    domain_output_dir.mkdir(parents=True, exist_ok=True)
    target_video_file = domain_output_dir / f"{agent_name}.mp4"

    AUTHENTIC_CUTOFF = 1788961200  # 2026-09-09 13:40:00 UTC (enhanced slower typing, natural scroll, 10x speedup cutoff)
    if skip_existing and target_video_file.exists() and target_video_file.stat().st_mtime > AUTHENTIC_CUTOFF:
        print(f"⏩ Skipping {agent_name} (already recorded with enhanced 4-turn format: {target_video_file.stat().st_size / (1024*1024):.1f} MB)", flush=True)
        try:
            generate_html_showcase(agent_name, domain=domain, output_dir=output_dir)
        except Exception:
            pass
        return target_video_file

    readme_path = REPO_ROOT / "agents" / domain / agent_name / "README.md"
    prompts = parse_agent_prompts(readme_path, agent_name)
    if not prompts:
        prompts = [f"Provide a comprehensive operational analysis and status report for {agent_name}."]

    worker_dir = recorder_base_dir if worker_id == 0 else (recorder_base_dir.parent / f"google-chrome-demo-recorder-{worker_id}")
    sync_chrome_profile(worker_dir, profile_dir)

    temp_video_dir = domain_output_dir / f".tmp_video_{agent_name}_{int(time.time())}_{worker_id}"
    if temp_video_dir.exists():
        shutil.rmtree(str(temp_video_dir))
    temp_video_dir.mkdir(parents=True, exist_ok=True)

    cat_entry = get_catalog_entry(agent_name)
    display_name = cat_entry.get("name", agent_name.replace("_", " ").title())
    clean_name = display_name.split(":")[-1].strip() if ":" in display_name else display_name

    res = RESOLUTION_CONFIGS["1080p"]
    w, h = res["width"], res["height"]

    print("\n" + "=" * 60, flush=True)
    print(f"🎬 RECORDING AUTHENTIC GE DEMO: {clean_name} ({agent_name})", flush=True)
    print(f"📁 Domain: {domain} | Worker: {worker_id}", flush=True)
    print(f"🎯 Target Video: {target_video_file}", flush=True)
    print(f"📝 Prompts ({min(turns_count, len(prompts))} turns):", flush=True)
    for idx, p in enumerate(prompts[:turns_count], 1):
        print(f"   {idx}. {p}", flush=True)
    print("=" * 60, flush=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(worker_dir),
            channel="chrome",
            headless=headless,
            record_video_dir=str(temp_video_dir),
            record_video_size=res,
            viewport=res,
            device_scale_factor=1.0,
            ignore_default_args=["--password-store=basic", "--use-mock-keychain"],
            args=[
                f"--profile-directory={profile_dir}",
                "--password-store=detect",
                "--force-device-scale-factor=1.0",
                "--disable-blink-features=AutomationControlled",
                "--no-default-browser-check",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                f"--window-size={w},{h}"
            ]
        )

        page = context.pages[0] if context.pages else await context.new_page()

        try:
            print(f"🔗 Navigating to Gemini Enterprise: {ge_url}", flush=True)
            await page.goto(ge_url, wait_until="networkidle", timeout=45000)
            await asyncio.sleep(2.5)

            # 1. Click "Agents" tab in sidebar
            print("👉 Step 1: Navigating to Agents tab...", flush=True)
            agents_clicked = False
            left_elements = await page.locator("a:visible, button:visible, div[role='button']:visible, li:visible").all()
            for el in left_elements:
                box = await el.bounding_box()
                if box and box["x"] < 250:
                    txt = (await el.text_content() or "").strip()
                    if txt == "Agents" or txt.startswith("Agents"):
                        await el.click()
                        agents_clicked = True
                        break
            if not agents_clicked:
                agents_btn = page.locator("text=Agents").first
                await agents_btn.click()
            await asyncio.sleep(2.5)

            # 2. Search for the agent in center search box (with readable typing)
            print(f"👉 Step 2: Searching for '{clean_name}'...", flush=True)
            candidate_inputs = await page.locator("input:visible").all()
            searched = False
            for inp in candidate_inputs:
                box = await inp.bounding_box()
                if box and box["x"] > 250 and box["y"] < 350:
                    await inp.click()
                    await inp.type(clean_name, delay=typing_delay)
                    searched = True
                    break
            if not searched:
                search_box = page.locator("input[placeholder*='Search' i]:visible").last
                await search_box.click()
                await search_box.type(clean_name, delay=typing_delay)
            await asyncio.sleep(2.5)

            # 3. Click the agent card
            print(f"👉 Step 3: Selecting agent card for '{clean_name}'...", flush=True)
            cards = await page.locator("[role='button']:visible, mat-card:visible, a:visible, div:visible").all()
            card_clicked = False
            keywords = [k for k in clean_name.lower().split() if len(k) > 3]
            for el in cards:
                box = await el.bounding_box()
                if box and box["x"] > 250 and box["y"] > 180 and box["width"] > 100:
                    txt = (await el.text_content() or "").strip().lower()
                    if all(k in txt for k in keywords[:2]):
                        await el.click()
                        card_clicked = True
                        break
            if not card_clicked:
                card = page.locator(f"text={clean_name}").first
                await card.click()
            await asyncio.sleep(3.5)

            # 4. Multi-turn execution (up to turns_count prompts)
            rec_start_time = time.time()
            wait_intervals: list[tuple[float, float]] = []

            for idx, prompt_text in enumerate(prompts[:turns_count], 1):
                print(f"👉 Turn {idx}/{turns_count}: Submitting prompt...", flush=True)
                input_box = page.locator("div[contenteditable='true']:visible, textarea:visible").last
                await input_box.wait_for(state="visible", timeout=15000)
                await input_box.click()
                await asyncio.sleep(0.3)
                
                # Clear any lingering text
                await input_box.press("ControlOrMeta+a")
                await input_box.press("Backspace")
                await asyncio.sleep(0.2)
                
                # Slower typing so the viewer can read clearly
                await input_box.press_sequentially(prompt_text, delay=typing_delay)
                # Pause slightly after typing completes so viewer can see the complete text
                await asyncio.sleep(0.6)

                send_btn = page.locator(
                    "button[aria-label*='Send' i]:visible, button[aria-label*='Submit' i]:visible, button:visible:has(mat-icon:has-text('arrow_upward'))"
                ).last
                if await send_btn.is_visible():
                    await send_btn.click()
                else:
                    await input_box.press("Enter")
                
                # Timestamp when waiting period begins
                wait_start = time.time() - rec_start_time
                print(f"   ✓ Turn {idx} prompt sent. Waiting for agent streaming response...", flush=True)

                # Wait for stop button to appear (generation active)
                visible_stops = page.locator("button[aria-label*='Stop' i]:visible, button:has(mat-icon:has-text('stop')):visible")
                for _ in range(25):
                    if await visible_stops.count() > 0:
                        break
                    await asyncio.sleep(0.4)

                start_stream_time = time.time()
                while True:
                    if (await visible_stops.count()) == 0:
                        print(f"   ✓ Turn {idx} completed in {time.time() - start_stream_time:.1f}s.", flush=True)
                        break
                    if time.time() - start_stream_time > 120:
                        print(f"   ⚠️ Turn {idx} reached timeout (120s). Proceeding...", flush=True)
                        break
                    await asyncio.sleep(0.8)

                # Timestamp when waiting period completes
                wait_end = time.time() - rec_start_time
                wait_intervals.append((wait_start, wait_end))

                # Smooth, natural-pace scroll down through the response to the bottom
                print(f"   📜 Scrolling down through Turn {idx} response at natural pace...", flush=True)
                center_x = int(w * 0.55)
                center_y = int(h * 0.5)
                await page.mouse.move(center_x, center_y)
                await asyncio.sleep(0.3)

                # Incremental natural mouse wheel scrolling
                for _ in range(16):
                    await page.mouse.wheel(0, 85)
                    await asyncio.sleep(0.08)

                # Ensure container is smoothly aligned to the absolute bottom
                await page.evaluate("""() => {
                    const scrollables = Array.from(document.querySelectorAll('*')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
                    });
                    for (const el of scrollables) {
                        el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
                    }
                }""")

                # Pause at bottom for human reading comprehension before moving to next turn
                await asyncio.sleep(read_pause)

            # 5. Smooth mouse scroll walkthrough across the multi-turn session
            print("👉 Step 5: Smooth mouse scroll walkthrough across all turns...", flush=True)
            center_x = int(w * 0.55)
            center_y = int(h * 0.5)
            await page.mouse.move(center_x, center_y)
            await asyncio.sleep(0.5)

            # Scroll up smoothly to inspect previous turns
            for _ in range(30):
                await page.mouse.wheel(0, -180)
                await asyncio.sleep(0.04)
            await asyncio.sleep(1.8)

            # Scroll down smoothly to return to latest turn
            for _ in range(30):
                await page.mouse.wheel(0, 180)
                await asyncio.sleep(0.04)
            await asyncio.sleep(1.8)

            print("👉 Step 6: Finalizing recording...", flush=True)
            await asyncio.sleep(1.2)
            await context.close()

        except Exception as e:
            print(f"❌ Error during recording of {agent_name}: {e}", flush=True)
            await context.close()
            return None

    # Transcode WebM to MP4 with accelerated waiting intervals
    webms = list(temp_video_dir.glob("*.webm"))
    if not webms:
        print(f"❌ No WebM file recorded for {agent_name}", flush=True)
        return None

    raw_webm = webms[0]
    ok = convert_webm_to_mp4(
        raw_webm,
        target_video_file,
        wait_intervals=wait_intervals,
        speedup_factor=speedup_factor
    )
    shutil.rmtree(str(temp_video_dir), ignore_errors=True)

    if ok and target_video_file.exists():
        print(f"✅ Successfully created {target_video_file} ({target_video_file.stat().st_size / (1024*1024):.1f} MB)", flush=True)
        try:
            generate_html_showcase(agent_name, domain=domain, output_dir=output_dir)
        except Exception as err:
            print(f"⚠️ HTML showcase generation error: {err}", flush=True)

        if upload:
            try:
                subprocess.run(
                    ["gsutil", "cp", str(target_video_file), f"gs://utilities-agents-demos/{domain}/{target_video_file.name}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                html_file = domain_output_dir / f"{agent_name}.html"
                if html_file.exists():
                    subprocess.run(
                        ["gsutil", "cp", str(html_file), f"gs://utilities-agents-demos/{domain}/{html_file.name}"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                print(f"☁️ Uploaded {agent_name} to gs://utilities-agents-demos/{domain}/", flush=True)
            except Exception as up_err:
                print(f"⚠️ GCS upload error: {up_err}", flush=True)

        return target_video_file
    else:
        print(f"❌ Failed to produce MP4 for {agent_name}", flush=True)
        return None


async def run_batch(
    agents_to_run: list[dict],
    output_dir: Path,
    concurrency: int = 1,
    turns: int = 4,
    typing_delay: int = 35,
    speedup: float = 10.0,
    read_pause: float = 2.2,
    skip_existing: bool = False,
    upload: bool = False
):
    semaphore = asyncio.Semaphore(concurrency)

    async def worker(agent_info: dict, wid: int):
        async with semaphore:
            return await record_single_agent(
                agent_name=agent_info["id"],
                domain=agent_info["domain"],
                output_dir=output_dir,
                worker_id=wid,
                turns_count=turns,
                typing_delay=typing_delay,
                read_pause=read_pause,
                speedup_factor=speedup,
                skip_existing=skip_existing,
                upload=upload
            )

    tasks = []
    for idx, a in enumerate(agents_to_run):
        wid = idx % concurrency
        tasks.append(worker(a, wid))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    successes = sum(1 for r in results if isinstance(r, Path) and r.exists())
    print(f"\n🎉 Batch completed: {successes}/{len(agents_to_run)} videos successfully recorded!")


def main():
    parser = argparse.ArgumentParser(description="Record authentic Gemini Enterprise agent demo videos.")
    parser.add_argument("--name", type=str, help="Agent name (e.g. drone_inspection_image_processor)")
    parser.add_argument("--domain", type=str, help="Sub-domain name (e.g. asset_management)")
    parser.add_argument("--domain-filter", type=str, help="Filter by sub-domain for batch recording")
    parser.add_argument("--all", action="store_true", help="Record all agents in the catalog")
    parser.add_argument("--turns", type=int, default=4, help="Number of turns to record per agent (default: 4)")
    parser.add_argument("--typing-delay", type=int, default=35, help="Keystroke typing delay in ms (default: 35)")
    parser.add_argument("--speedup", type=float, default=10.0, help="Acceleration factor for agent waiting periods (default: 10.0)")
    parser.add_argument("--read-pause", type=float, default=2.2, help="Pause after response scroll in seconds (default: 2.2)")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent browser instances (default: 1)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip agents with existing MP4")
    parser.add_argument("--headless", action="store_true", default=True, help="Run Chrome headless (default: True)")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="Run Chrome headed")
    parser.add_argument("--upload", action="store_true", help="Upload recorded videos to GCS gs://utilities-agents-demos/")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "demos", help="Output directory")
    args = parser.parse_args()

    if args.name:
        domain = args.domain or resolve_agent_domain(args.name)
        asyncio.run(
            record_single_agent(
                agent_name=args.name,
                domain=domain,
                output_dir=args.output_dir,
                headless=args.headless,
                turns_count=args.turns,
                typing_delay=args.typing_delay,
                read_pause=args.read_pause,
                speedup_factor=args.speedup,
                skip_existing=args.skip_existing,
                upload=args.upload
            )
        )
    elif args.domain_filter or args.all:
        cat_file = REPO_ROOT / "web" / "catalog.json"
        if not cat_file.exists():
            print("❌ web/catalog.json not found.")
            sys.exit(1)
        with open(cat_file, "r") as f:
            agents = json.load(f)

        if args.domain_filter:
            agents = [a for a in agents if a["domain"] == args.domain_filter]

        print(f"📋 Queued {len(agents)} agents for recording (concurrency={args.concurrency}, turns={args.turns}, speedup={args.speedup}x, typing_delay={args.typing_delay}ms)...")
        asyncio.run(
            run_batch(
                agents_to_run=agents,
                output_dir=args.output_dir,
                concurrency=args.concurrency,
                turns=args.turns,
                typing_delay=args.typing_delay,
                speedup=args.speedup,
                read_pause=args.read_pause,
                skip_existing=args.skip_existing,
                upload=args.upload
            )
        )
    else:
        print("Please provide --name <agent_name>, --domain-filter <domain>, or --all")
        sys.exit(1)

    if args.upload:
        print("\n☁️ Uploading recorded demo videos to gs://utilities-agents-demos/...")
        cmd = ["gsutil", "-m", "cp", "-r", str(args.output_dir) + "/*", "gs://utilities-agents-demos/"]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print("✅ Successfully uploaded demos to GCS!")
        else:
            print(f"⚠️ GCS upload returned exit code {res.returncode}")

if __name__ == "__main__":
    main()
