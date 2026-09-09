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


def convert_webm_to_mp4(webm_path: Path, mp4_path: Path) -> bool:
    """Converts recorded webm video to high-quality universal MP4 using ffmpeg."""
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


async def record_single_agent(
    agent_name: str,
    domain: str,
    output_dir: Path,
    ge_url: str = DEFAULT_GE_URL,
    profile_dir: str = DEFAULT_CHROME_PROFILE_DIR,
    recorder_base_dir: Path = DEFAULT_BASE_RECORDER_DIR,
    worker_id: int = 0,
    headless: bool = True,
    turns_count: int = 1,
    read_pause: float = 3.5,
    skip_existing: bool = False,
    upload: bool = False
) -> Path | None:
    from playwright.async_api import async_playwright

    domain_output_dir = output_dir / domain
    domain_output_dir.mkdir(parents=True, exist_ok=True)
    target_video_file = domain_output_dir / f"{agent_name}.mp4"

    AUTHENTIC_CUTOFF = 1788940800  # 2026-09-09 08:00:00 UTC
    if skip_existing and target_video_file.exists() and target_video_file.stat().st_mtime > AUTHENTIC_CUTOFF:
        print(f"⏩ Skipping {agent_name} (already authentically recorded: {target_video_file.stat().st_size / (1024*1024):.1f} MB)", flush=True)
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

            # 2. Search for the agent in center search box
            print(f"👉 Step 2: Searching for '{clean_name}'...", flush=True)
            candidate_inputs = await page.locator("input:visible").all()
            searched = False
            for inp in candidate_inputs:
                box = await inp.bounding_box()
                if box and box["x"] > 250 and box["y"] < 350:
                    await inp.click()
                    await inp.type(clean_name, delay=20)
                    searched = True
                    break
            if not searched:
                search_box = page.locator("input[placeholder*='Search' i]:visible").last
                await search_box.click()
                await search_box.type(clean_name, delay=20)
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

            # 4. Multi-turn execution
            for idx, prompt_text in enumerate(prompts[:turns_count], 1):
                print(f"👉 Turn {idx}/{turns_count}: Submitting prompt...", flush=True)
                input_box = page.locator("div[contenteditable='true']:visible, textarea:visible").last
                await input_box.wait_for(state="visible", timeout=15000)
                await input_box.click()
                await asyncio.sleep(0.4)
                await input_box.press_sequentially(prompt_text, delay=12)
                await asyncio.sleep(0.6)

                send_btn = page.locator(
                    "button[aria-label*='Send' i]:visible, button[aria-label*='Submit' i]:visible, button:visible:has(mat-icon:has-text('arrow_upward'))"
                ).last
                if await send_btn.is_visible():
                    await send_btn.click()
                else:
                    await input_box.press("Enter")
                print(f"   ✓ Turn {idx} prompt sent. Waiting for agent streaming response...", flush=True)

                # Wait for stop button to appear (generation active)
                visible_stops = page.locator("button[aria-label*='Stop' i]:visible, button:has(mat-icon:has-text('stop')):visible")
                for _ in range(30):
                    if await visible_stops.count() > 0:
                        break
                    await asyncio.sleep(0.5)

                start_stream_time = time.time()
                while True:
                    if (await visible_stops.count()) == 0:
                        print(f"   ✓ Turn {idx} completed in {time.time() - start_stream_time:.1f}s.", flush=True)
                        break
                    if time.time() - start_stream_time > 120:
                        print(f"   ⚠️ Turn {idx} reached timeout (120s). Proceeding...", flush=True)
                        break
                    await asyncio.sleep(1.0)

                await asyncio.sleep(read_pause)

            # 5. Smooth mouse scroll walkthrough
            print("👉 Step 5: Smooth mouse scroll walkthrough...", flush=True)
            center_x = int(w * 0.55)
            center_y = int(h * 0.5)
            await page.mouse.move(center_x, center_y)
            await asyncio.sleep(0.5)

            # Scroll up smoothly
            for _ in range(25):
                await page.mouse.wheel(0, -180)
                await asyncio.sleep(0.04)
            await asyncio.sleep(2.5)

            # Scroll down smoothly
            for _ in range(25):
                await page.mouse.wheel(0, 180)
                await asyncio.sleep(0.04)
            await asyncio.sleep(2.5)

            print("👉 Step 6: Finalizing recording...", flush=True)
            await asyncio.sleep(2.0)
            await context.close()

        except Exception as e:
            print(f"❌ Error during recording of {agent_name}: {e}", flush=True)
            await context.close()
            return None

    # Transcode WebM to MP4
    webms = list(temp_video_dir.glob("*.webm"))
    if not webms:
        print(f"❌ No WebM file recorded for {agent_name}", flush=True)
        return None

    raw_webm = webms[0]
    ok = convert_webm_to_mp4(raw_webm, target_video_file)
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


async def run_batch(agents_to_run: list[dict], output_dir: Path, concurrency: int = 1, turns: int = 1, skip_existing: bool = False, upload: bool = False):
    semaphore = asyncio.Semaphore(concurrency)

    async def worker(agent_info: dict, wid: int):
        async with semaphore:
            return await record_single_agent(
                agent_name=agent_info["id"],
                domain=agent_info["domain"],
                output_dir=output_dir,
                worker_id=wid,
                turns_count=turns,
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
    parser.add_argument("--turns", type=int, default=1, help="Number of turns to record per agent (default: 1)")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent browser instances (default: 1)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip agents with existing MP4 > 500KB")
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

        print(f"📋 Queued {len(agents)} agents for recording (concurrency={args.concurrency}, turns={args.turns})...")
        asyncio.run(
            run_batch(
                agents_to_run=agents,
                output_dir=args.output_dir,
                concurrency=args.concurrency,
                turns=args.turns,
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
