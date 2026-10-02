import asyncio
import aiohttp
import time
import subprocess
import os
import shutil
import base64
import json

ffmpeg_bin = r'C:\ZKBioTime\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
work_dir = r'c:\Users\user\Desktop\Uni\gin400'
temp_frames_dir = os.path.join(work_dir, 'temp_video_render')
os.makedirs(temp_frames_dir, exist_ok=True)

# Scene durations
AUDIO_DURATIONS = [29.81, 35.16, 43.15, 38.74, 43.15, 34.4, 32.89, 37.72, 41.25]

async def capture_and_encode():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    port = 9788
    user_data = os.path.join(work_dir, 'chrome_render_profile')
    
    cmd = [
        chrome,
        '--headless=new',
        f'--user-data-dir={user_data}',
        f'--remote-debugging-port={port}',
        '--window-size=1280,720',
        '--disable-gpu',
        '--no-sandbox',
        'file:///c:/Users/user/Desktop/Uni/gin400/query_optimization_video.html'
    ]
    proc = subprocess.Popen(cmd)
    scene_mp4s = []
    
    try:
        await asyncio.sleep(2.5)
        async with aiohttp.ClientSession() as s:
            r = await s.get(f'http://localhost:{port}/json')
            tabs = await r.json()
            ws_url = [t['webSocketDebuggerUrl'] for t in tabs if 'query_optimization' in t.get('url', '')][0]
            
            async with s.ws_connect(ws_url) as ws:
                inject_js = """
                window.renderFullFrame = function(scIdx, t) {
                    const sc = scenes[scIdx];
                    selectScene(scIdx, false);
                    sc.render(ctx, t, canvas.width, canvas.height);
                    
                    const w = canvas.width;
                    const h = canvas.height;
                    
                    ctx.save();
                    
                    // For scene 0, draw section title since scene 0 has no built-in header
                    if (scIdx === 0) {
                        ctx.font = "bold 20px sans-serif";
                        ctx.fillStyle = "#ffffff";
                        ctx.textAlign = "left";
                        ctx.textBaseline = "alphabetic";
                        ctx.fillText("1. The Query Processing Architecture", 60, 60);
                    }
                    
                    // Top right formula chip
                    const formulas = [
                        "O(Cost) = Est(Disk I/O) + Est(CPU)",
                        "sl = 1/V(A,R) | A1=[b/2], A2=b",
                        "A3(Prim/Eq) = HT+1 | A4(Range) = HT+b",
                        "Simple NL: bR + bR·bS | Block: bR + ⌈bR/(B-2)⌉·bS",
                        "Sort-Merge Cost = 3·(bR + bS)",
                        "Equivalence: σ_θ(R ⋈ S) ≡ (σ_θ(R)) ⋈ S",
                        "Dynamic Programming: Left-Deep O(3^n)",
                        "b = ⌈r / f⌉ | Blocks = r / Blocking Factor",
                        "Mastery: Cost Estimation + Equivalence + Joins"
                    ];
                    
                    const formulaText = formulas[scIdx] || sc.hudCost || "";
                    if (formulaText) {
                        ctx.font = "bold 13px Inter, monospace, sans-serif";
                        const fWidth = ctx.measureText(formulaText).width + 30;
                        const chipX = w - fWidth - 30;
                        const chipY = 22;
                        const chipH = 34;
                        
                        ctx.fillStyle = "rgba(15, 23, 42, 0.90)";
                        ctx.strokeStyle = "rgba(168, 85, 247, 0.5)";
                        ctx.lineWidth = 1.2;
                        ctx.beginPath();
                        ctx.roundRect(chipX, chipY, fWidth, chipH, 8);
                        ctx.fill();
                        ctx.stroke();
                        
                        ctx.fillStyle = "#c084fc";
                        ctx.textAlign = "center";
                        ctx.textBaseline = "middle";
                        ctx.fillText(formulaText, chipX + fWidth / 2, chipY + chipH / 2);
                    }
                    
                    // Bottom Subtitles Pill
                    const cues = SUBTITLES_DATA[scIdx] || [];
                    let activeSent = null;
                    for (let c of cues) {
                        if (t >= c.start && t <= c.end + 0.3) {
                            activeSent = c;
                            break;
                        }
                    }
                    
                    if (activeSent) {
                        ctx.font = "bold 16px Inter, system-ui, sans-serif";
                        ctx.textBaseline = "middle";
                        
                        // Break words into lines (max line width 1020px)
                        const maxLineWidth = 1020;
                        const lines = [];
                        let currentLine = [];
                        let currentLineWidth = 0;
                        
                        for (let wItem of activeSent.words) {
                            const wordW = ctx.measureText(wItem.word + " ").width;
                            if (currentLineWidth + wordW > maxLineWidth && currentLine.length > 0) {
                                lines.push({ words: currentLine, totalW: currentLineWidth });
                                currentLine = [wItem];
                                currentLineWidth = wordW;
                            } else {
                                currentLine.push(wItem);
                                currentLineWidth += wordW;
                            }
                        }
                        if (currentLine.length > 0) {
                            lines.push({ words: currentLine, totalW: currentLineWidth });
                        }
                        
                        const pillW = Math.min(1140, Math.max(...lines.map(l => l.totalW)) + 60);
                        const lineH = 26;
                        const pillH = lines.length === 1 ? 52 : (lines.length * lineH + 24);
                        const pillX = (w - pillW) / 2;
                        const pillY = h - pillH - 20;
                        
                        // Background pill
                        ctx.fillStyle = "rgba(10, 15, 29, 0.94)";
                        ctx.strokeStyle = "rgba(56, 189, 248, 0.45)";
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.roundRect(pillX, pillY, pillW, pillH, 10);
                        ctx.fill();
                        ctx.stroke();
                        
                        // Render words line by line
                        const firstLineY = lines.length === 1 ? (pillY + pillH / 2) : (pillY + 22);
                        
                        lines.forEach((ln, lIdx) => {
                            const lineY = firstLineY + lIdx * lineH;
                            let startWordX = (w - ln.totalW) / 2;
                            ctx.textAlign = "left";
                            
                            for (let wm of ln.words) {
                                const wordText = wm.word + " ";
                                const wordW = ctx.measureText(wordText).width;
                                if (t >= wm.start && t <= wm.end) {
                                    ctx.fillStyle = "#fbbf24";
                                    ctx.shadowColor = "#f59e0b";
                                    ctx.shadowBlur = 10;
                                    ctx.font = "bold 17px Inter, system-ui, sans-serif";
                                } else if (t > wm.end) {
                                    ctx.fillStyle = "#ffffff";
                                    ctx.shadowBlur = 0;
                                    ctx.font = "16px Inter, system-ui, sans-serif";
                                } else {
                                    ctx.fillStyle = "#94a3b8";
                                    ctx.shadowBlur = 0;
                                    ctx.font = "16px Inter, system-ui, sans-serif";
                                }
                                ctx.fillText(wm.word, startWordX, lineY);
                                startWordX += wordW;
                            }
                        });
                        ctx.shadowBlur = 0;
                    }
                    ctx.restore();
                    return canvas.toDataURL("image/jpeg", 0.90);
                };
                """
                await ws.send_json({
                    'id': 1,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': inject_js}
                })
                await ws.receive_json()
                
                fps = 2
                msg_counter = 10
                
                for sc_idx in range(9):
                    dur = AUDIO_DURATIONS[sc_idx]
                    total_frames = int(dur * fps) + 1
                    sc_temp_dir = os.path.join(temp_frames_dir, f'sc_{sc_idx}')
                    os.makedirs(sc_temp_dir, exist_ok=True)
                    
                    t_start = time.time()
                    print(f"🎬 Rendering Scene {sc_idx + 1}/9 ({dur:.1f}s, {total_frames} frames)...")
                    
                    for f_idx in range(total_frames):
                        t_frame = f_idx / fps
                        msg_counter += 1
                        await ws.send_json({
                            'id': msg_counter,
                            'method': 'Runtime.evaluate',
                            'params': {'expression': f'window.renderFullFrame({sc_idx}, {t_frame:.2f})'}
                        })
                        res = await ws.receive_json()
                        val = res.get('result', {}).get('result', {}).get('value', '')
                        if val.startswith('data:image/jpeg;base64,'):
                            raw = base64.b64decode(val.split(',')[1])
                            f_path = os.path.join(sc_temp_dir, f'frame_{f_idx:04d}.jpg')
                            with open(f_path, 'wb') as f_out:
                                f_out.write(raw)
                                
                    t_render = time.time() - t_start
                    print(f"   ✓ Captured in {t_render:.1f}s. Encoding video track...")
                    
                    # Encode scene MP4 with FFmpeg
                    audio_path = os.path.join(work_dir, 'audio', f'scene_{sc_idx}.mp3')
                    out_sc_mp4 = os.path.join(temp_frames_dir, f'scene_{sc_idx}.mp4')
                    cmd_ffmpeg = [
                        ffmpeg_bin, '-y',
                        '-framerate', str(fps),
                        '-i', os.path.join(sc_temp_dir, 'frame_%04d.jpg'),
                        '-i', audio_path,
                        '-c:v', 'libx264', '-preset', 'fast', '-crf', '19',
                        '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '192k',
                        '-shortest',
                        out_sc_mp4
                    ]
                    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    scene_mp4s.append(out_sc_mp4)
                    
                    # Clean up scene frame images
                    shutil.rmtree(sc_temp_dir)
                    print(f"   ✓ Scene {sc_idx + 1} MP4 ready!")
                    
    finally:
        proc.terminate()
        await asyncio.sleep(0.5)
        if os.path.exists(user_data):
            try: shutil.rmtree(user_data)
            except: pass
            
    # Concatenate all 9 scenes
    print("🔗 Concatenating all 9 scenes into final masterclass MP4...")
    concat_txt_path = os.path.join(temp_frames_dir, 'concat_list.txt')
    with open(concat_txt_path, 'w', encoding='utf-8') as f:
        for s_mp4 in scene_mp4s:
            p = s_mp4.replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    final_mp4 = os.path.join(work_dir, 'query_optimization_masterclass.mp4')
    cmd_concat = [
        ffmpeg_bin, '-y',
        '-f', 'concat', '-safe', '0',
        '-i', concat_txt_path,
        '-c', 'copy',
        final_mp4
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Clean up temp
    shutil.rmtree(temp_frames_dir)
    
    file_size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print(f"🎉 SUCCESS! Final Masterclass MP4 compiled successfully!")
    print(f"📁 Output: {final_mp4}")
    print(f"📊 File Size: {file_size_mb:.2f} MB")
    return final_mp4

if __name__ == '__main__':
    asyncio.run(capture_and_encode())
