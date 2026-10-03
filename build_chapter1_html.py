import json
import os

work_dir = r'c:\Users\user\Desktop\Uni\gin400'
chap1_data_path = os.path.join(work_dir, 'chap1_data.json')
output_html_path = os.path.join(work_dir, 'chapter1.html')

with open(chap1_data_path, 'r', encoding='utf-8') as f:
    scenes_data = json.load(f)

print(f"Loaded {len(scenes_data)} scenes from chap1_data.json")

# Extract audio tracks, durations, and subtitles
audio_tracks = [sc["audioUri"] for sc in scenes_data]
audio_durations = [sc["duration"] for sc in scenes_data]
subtitles_data = [sc.get("subtitles", sc.get("sentences", [])) for sc in scenes_data]

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Physical Storage, File Structures & Indexing - Studio AI Masterclass (Chapter 1)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @keyframes pulseGlow {
      0%, 100% { filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.6)); }
      50% { filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.8)); }
    }
    .video-viewport {
      position: relative;
      background: radial-gradient(circle at 50% 30%, #082f49 0%, #020617 100%);
      aspect-ratio: 16 / 9;
      overflow: hidden;
    }
    .custom-scroll::-webkit-scrollbar {
      width: 6px;
    }
    .custom-scroll::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.6);
    }
    .custom-scroll::-webkit-scrollbar-thumb {
      background: #06b6d4;
      border-radius: 3px;
    }
    .wave-bar {
      animation: waveAnim 0.8s ease-in-out infinite alternate;
    }
    @keyframes waveAnim {
      0% { height: 4px; }
      100% { height: 16px; }
    }
    .active-word {
      color: #38bdf8;
      font-weight: 800;
      transform: scale(1.12);
      background: rgba(56, 189, 248, 0.22);
      border: 1px solid rgba(56, 189, 248, 0.5);
      border-radius: 4px;
      padding: 0 4px;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.7);
      display: inline-block;
      transition: all 0.08s ease-out;
    }
    .spoken-word {
      color: #ffffff;
      font-weight: 600;
      opacity: 0.95;
      display: inline-block;
      transition: all 0.08s ease-out;
    }
    .pending-word {
      color: #94a3b8;
      font-weight: 400;
      opacity: 0.5;
      display: inline-block;
      transition: all 0.08s ease-out;
    }
  </style>
  <!-- KaTeX for Beautiful Scientific & Database Math Rendering -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-cyan-600 selection:text-white">

  <!-- Header Navigation Bar -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-3 flex items-center justify-between shadow-lg">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/30">
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7c0-2-1.5-3-3.5-3h-9C5.5 4 4 5 4 7zM9 4v16M15 4v16M4 11h16M4 16h16"/>
        </svg>
      </div>
      <div>
        <h1 class="font-bold text-lg text-white leading-tight flex items-center gap-2">
          Advanced Database Systems
          <span class="bg-cyan-900/80 text-cyan-300 text-xs px-2.5 py-0.5 rounded-full border border-cyan-700">Chapter 1</span>
        </h1>
        <p class="text-xs text-slate-400">Physical Storage, File Structures & Indexing &bull; High-Definition Neural Masterclass</p>
      </div>
    </div>
    <div class="flex items-center gap-3">
      <a href="index.html" class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 transition shadow">
        <span>🏠</span> <span>Course Index</span>
      </a>
      <a href="chapter2.html" class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border border-blue-800/80 bg-blue-950/60 hover:bg-blue-900/80 text-blue-300 transition shadow">
        <span>⚡</span> <span>Chapter 2</span>
      </a>
      <div class="flex items-center gap-2 bg-emerald-950/70 border border-emerald-700/60 px-3 py-1.5 rounded-lg text-emerald-300 text-xs shadow hidden md:flex">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="font-semibold text-emerald-300">Studio AI Voice</span>
      </div>
      <button id="toggleSandboxBtn" class="flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-lg border border-cyan-700 bg-cyan-950/60 hover:bg-cyan-900/80 text-cyan-300 transition shadow">
        <span>🧮</span> Storage & Index Sandbox
      </button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

    <!-- Video Theater Section (8 cols on large screens) -->
    <div class="lg:col-span-8 flex flex-col gap-3">
      <!-- Animated Canvas Screen Container -->
      <div id="videoContainer" class="video-viewport rounded-2xl border border-slate-800 shadow-2xl relative group">
        
        <!-- Canvas for Dynamic 60fps Graphics -->
        <canvas id="animCanvas" class="w-full h-full block absolute inset-0 z-0"></canvas>

        <!-- Dynamic Scene Title Badge -->
        <div class="absolute top-4 left-4 z-20 flex items-center gap-2 bg-slate-900/85 backdrop-blur border border-slate-700/80 px-3 py-1.5 rounded-lg shadow-md">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
          <span id="sceneBadgeText" class="text-xs font-semibold text-slate-200 uppercase tracking-wider">Scene 1: Disk Geometry</span>
        </div>

        <!-- Live Synchronized LaTeX Formula Spotlight Banner -->
        <div id="liveFormulaCard" class="absolute top-14 left-4 z-20 max-w-sm md:max-w-lg bg-slate-950/90 backdrop-blur-md border border-cyan-500/40 hover:border-cyan-400 rounded-xl px-3.5 py-1.5 shadow-2xl transition-all duration-300 pointer-events-auto flex items-center gap-3">
          <div class="flex items-center gap-1.5 text-cyan-400 font-mono text-[10px] sm:text-xs font-bold shrink-0 uppercase tracking-wider">
            <span class="text-sm">📐</span> <span class="hidden sm:inline">FORMULA:</span>
          </div>
          <div id="liveFormulaMath" class="text-xs sm:text-sm text-yellow-300 font-serif overflow-x-auto whitespace-nowrap custom-scroll py-0.5 flex-1">
            <!-- Dynamically populated KaTeX formula -->
          </div>
          <button id="toggleFormulaBtn" class="text-slate-400 hover:text-white text-xs shrink-0 px-1" title="Toggle Formula Banner">✕</button>
        </div>

        <!-- Metric HUD in Top Right (includes live topic badge) -->
        <div id="hudBox" class="absolute top-4 right-4 z-20 bg-slate-900/85 backdrop-blur border border-slate-700/80 px-3 py-1.5 rounded-lg text-xs font-mono text-cyan-300 shadow-md flex items-center gap-3">
          <span id="hudTopic" class="text-yellow-400 font-bold hidden sm:inline">Disk Geometry</span>
          <span class="text-slate-500">|</span>
          <span>Cost: <span id="hudCost">O(Cost)</span></span>
          <div id="voiceVisualizer" class="flex items-end gap-0.5 h-4 opacity-70">
            <div class="w-1 bg-cyan-400 wave-bar" style="animation-delay: 0.1s;"></div>
            <div class="w-1 bg-cyan-400 wave-bar" style="animation-delay: 0.3s;"></div>
            <div class="w-1 bg-cyan-400 wave-bar" style="animation-delay: 0.2s;"></div>
            <div class="w-1 bg-cyan-400 wave-bar" style="animation-delay: 0.4s;"></div>
          </div>
        </div>

        <!-- Movable Floating Draggable CC Container -->
        <div id="onScreenCCContainer" class="absolute z-40 hidden select-none touch-none" style="left: 50%; bottom: 70px; transform: translateX(-50%); width: 88%; max-width: 680px; cursor: grab;">
          <div class="bg-slate-900/95 backdrop-blur-md border border-cyan-500/40 hover:border-cyan-400/80 text-white px-4 py-2.5 rounded-xl shadow-[0_12px_40px_rgba(0,0,0,0.85)] flex items-center gap-3 transition-colors">
            <!-- Drag Handle -->
            <div id="ccDragHandle" class="cursor-grab active:cursor-grabbing flex items-center gap-1.5 px-2 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 rounded border border-cyan-500/30 select-none shrink-0" title="Click and drag anywhere to move CC">
              <svg class="w-3.5 h-3.5 text-cyan-400 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10 9h4V6h3l-5-5-5 5h3v3zm-1 1H6V7l-5 5 5 5v-3h3v-4zm14 2l-5-5v3h-3v4h3v3l5-5zm-9 3h-4v3H7l5 5 5-5h-3v-3z"/>
              </svg>
              <span class="text-[10px] font-mono font-bold text-cyan-400">CC</span>
              <span class="text-[9px] uppercase tracking-wider text-slate-400 font-mono hidden sm:inline">⋮⋮ DRAG</span>
            </div>
            <!-- Word-by-Word Karaoke Subtitles Box -->
            <div id="subtitlesBox" class="flex-1 text-center font-medium leading-relaxed tracking-wide text-xs sm:text-sm flex flex-wrap justify-center items-center gap-x-1.5 gap-y-0.5">
              Click Play to start the animated lecture.
            </div>
            <!-- Close Button -->
            <button id="closeOverlayCCBtn" class="text-slate-400 hover:text-white p-1 rounded hover:bg-slate-800 transition-colors text-xs shrink-0" title="Hide floating CC">✕</button>
          </div>
        </div>

        <!-- Video Overlay Control Bar -->
        <div class="absolute bottom-0 inset-x-0 z-30 bg-gradient-to-t from-slate-950 via-slate-950/90 to-transparent p-4 flex flex-col gap-2">
          <!-- Timeline Scrubber -->
          <div class="relative w-full h-2.5 bg-slate-800 rounded-full cursor-pointer group/bar flex items-center" id="timelineBar">
            <div id="timelineProgress" class="h-full bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-500 rounded-full relative" style="width: 0%;">
              <span class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 w-4 h-4 bg-white rounded-full shadow-lg scale-0 group-hover/bar:scale-100 transition-transform"></span>
            </div>
          </div>

          <!-- Controls Row -->
          <div class="flex items-center justify-between text-xs text-slate-300 pt-1">
            <div class="flex items-center gap-4">
              <!-- Play / Pause -->
              <button id="playBtn" class="w-9 h-9 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white flex items-center justify-center transition shadow-lg shadow-cyan-600/40 ring-2 ring-cyan-400/30">
                <svg id="playIcon" class="w-4 h-4 translate-x-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                <svg id="pauseIcon" class="w-4 h-4 hidden" fill="currentColor" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
              </button>

              <!-- Previous / Next Scene -->
              <button id="prevBtn" class="hover:text-white transition p-1" title="Previous Scene">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>
              </button>
              <button id="nextBtn" class="hover:text-white transition p-1" title="Next Scene">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
              </button>

              <!-- Timestamps -->
              <span class="font-mono text-slate-400">
                <span id="currentTime" class="text-white font-bold">00:00</span> / <span id="totalDuration">06:29</span>
              </span>

              <!-- Volume / Mute -->
              <button id="muteBtn" class="hover:text-white transition text-sm flex items-center gap-1.5" title="Toggle Mute">
                <span id="muteIcon">🔊</span>
              </button>
            </div>

            <!-- Right Controls: CC, Speed & Fullscreen -->
            <div class="flex items-center gap-3">
              <!-- On-Screen CC Toggle -->
              <button id="ccToggleBtn" class="px-2 py-0.5 rounded font-mono text-[11px] font-bold border border-slate-700 bg-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1" title="Toggle On-Screen Subtitle Overlay">
                <span>CC Overlay</span>
              </button>

              <!-- Export / Save Video Button -->
              <button id="exportVideoBtn" class="px-2.5 py-0.5 rounded font-mono text-[11px] font-bold border border-cyan-600/70 bg-cyan-950/80 text-cyan-400 hover:bg-cyan-900/90 hover:text-cyan-300 transition flex items-center gap-1.5 shadow-sm" title="Save / Export this scene or lecture as a video file (.webm / .mp4)">
                <span>💾</span> <span>Save / Export Video</span>
              </button>

              <div class="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded px-2 py-0.5">
                <span class="text-slate-400 text-[10px]">SPEED</span>
                <select id="speedSelect" class="bg-transparent text-white font-mono text-xs focus:outline-none cursor-pointer">
                  <option value="0.75" class="bg-slate-900">0.75x</option>
                  <option value="1" selected class="bg-slate-900">1.0x</option>
                  <option value="1.25" class="bg-slate-900">1.25x</option>
                  <option value="1.5" class="bg-slate-900">1.5x</option>
                  <option value="2" class="bg-slate-900">2.0x</option>
                </select>
              </div>

              <button id="fullscreenBtn" class="p-1 hover:text-white transition" title="Toggle Fullscreen">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0 0l-5-5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Dedicated Dynamic Karaoke Caption Bar (Below Video Viewport) -->
      <div id="captionBar" class="bg-slate-900/95 border border-slate-800 rounded-xl p-4 shadow-lg flex items-start gap-4">
        <div class="px-2.5 py-1 rounded bg-gradient-to-r from-cyan-900 to-blue-900 border border-cyan-700/80 text-[10px] font-mono text-cyan-300 shrink-0 mt-0.5 flex items-center gap-1.5 font-bold shadow-sm">
          <span>🎙️</span> <span>AI VOICE</span>
        </div>
        <div id="externalSubtitles" class="text-sm md:text-base text-slate-200 leading-relaxed font-medium flex-1 flex flex-wrap items-center gap-x-1.5 gap-y-1">
          Click Play to start the animated lecture with real-time word-by-word highlighted narration.
        </div>
      </div>

      <!-- Quick Scene Synopsis Card -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-md flex items-start gap-4">
        <div id="sceneIconContainer" class="w-12 h-12 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-xl text-cyan-400 shrink-0 shadow-inner">
          💽
        </div>
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <h3 id="currentSceneTitle" class="font-bold text-white text-base">Scene Title</h3>
            <span id="currentSceneDuration" class="text-xs font-mono text-cyan-400">Duration: 72s</span>
          </div>
          <p id="currentSceneSummary" class="text-xs text-slate-300 mt-1 leading-relaxed">
            Detailed breakdown will appear here.
          </p>
        </div>
      </div>
    </div>

    <!-- Chapter Playlist / Timeline Navigation (4 cols) -->
    <div class="lg:col-span-4 flex flex-col gap-4">
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-md flex flex-col h-[560px]">
        <!-- Sidebar Tabs: Scenes Playlist vs LaTeX Formula Reference -->
        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
          <div class="flex items-center gap-1 bg-slate-950/80 p-1 rounded-lg border border-slate-800">
            <button id="tabScenesBtn" class="px-3 py-1 rounded-md text-xs font-semibold bg-cyan-600 text-white transition-colors flex items-center gap-1.5 shadow-sm">
              <span>📚</span> <span>Scenes (6)</span>
            </button>
            <button id="tabFormulasBtn" class="px-3 py-1 rounded-md text-xs font-semibold text-slate-400 hover:text-white transition-colors flex items-center gap-1.5">
              <span>📐</span> <span>LaTeX Formulas</span>
            </button>
          </div>
          <span class="text-[10px] font-mono text-cyan-400 font-semibold hidden sm:inline">Studio Audio</span>
        </div>

        <!-- Tab 1: Playlist Item Scroll Container -->
        <div id="playlistContainer" class="flex-1 overflow-y-auto space-y-2 pr-1 custom-scroll">
          <!-- Populated by JavaScript -->
        </div>

        <!-- Tab 2: Full Chapter 1 LaTeX Formula Sheet (Scrollable) -->
        <div id="formulaSheetContainer" class="flex-1 overflow-y-auto space-y-3 pr-1 custom-scroll hidden text-xs">
          <!-- Populated by JavaScript with rich KaTeX equations -->
        </div>
      </div>
    </div>

  </main>

  <!-- Export Video Modal -->
  <div id="exportModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl flex flex-col gap-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">💾</span>
          <div>
            <h3 class="font-bold text-white text-base">Save & Export Masterclass Video</h3>
            <p class="text-xs text-slate-400">Choose how you would like to save the lecture</p>
          </div>
        </div>
        <button id="closeExportModalBtn" class="text-slate-400 hover:text-white text-2xl font-bold">&times;</button>
      </div>

      <div class="space-y-3">
        <!-- Option 1: Record Current Scene -->
        <button id="btnExportScene" class="w-full text-left p-3.5 rounded-xl border border-cyan-500/40 bg-cyan-950/40 hover:bg-cyan-900/60 hover:border-cyan-400 transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-cyan-300 group-hover:text-cyan-200 flex items-center gap-2">
              <span>🎬</span> <span>Record & Download Current Scene (.webm / .mp4)</span>
            </div>
            <p class="text-xs text-slate-400 mt-1">Records the active scene animation + studio voice and automatically downloads the video file.</p>
          </div>
          <span class="text-xs font-mono font-bold bg-cyan-600/40 text-cyan-200 px-2.5 py-1 rounded">START</span>
        </button>

        <!-- Option 2: Record Full Lecture -->
        <button id="btnExportFull" class="w-full text-left p-3.5 rounded-xl border border-blue-500/40 bg-blue-950/40 hover:bg-blue-900/60 hover:border-blue-400 transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-blue-300 group-hover:text-blue-200 flex items-center gap-2">
              <span>🌟</span> <span>Record Full 6-Scene Masterclass (All Chapters)</span>
            </div>
            <p class="text-xs text-slate-400 mt-1">Plays and records all 6 chapters sequentially into one complete high-definition video file.</p>
          </div>
          <span class="text-xs font-mono font-bold bg-blue-600/40 text-blue-200 px-2.5 py-1 rounded">START</span>
        </button>

        <!-- Option 3: Windows Instant 1080p Recording Shortcut -->
        <div class="p-3.5 rounded-xl border border-amber-500/30 bg-amber-950/30 text-xs space-y-1.5">
          <div class="font-bold text-amber-300 flex items-center gap-2">
            <span>⚡</span> <span>Windows 1-Click Screen Recorder (Instant 1080p MP4)</span>
          </div>
          <p class="text-slate-300 leading-relaxed">
            Press <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded font-mono text-amber-200 font-bold">Win + Alt + R</kbd> on your keyboard to instantly record this browser tab in 1080p 60fps MP4. Saved directly to your <code class="text-slate-200 font-mono">Videos\\Captures</code> folder!
          </p>
        </div>

        <!-- Option 4: File location on disk -->
        <div class="p-3 rounded-xl border border-slate-800 bg-slate-950/60 text-xs text-slate-400 flex items-center justify-between">
          <div class="truncate mr-2">
            <span class="block text-slate-300 font-semibold mb-0.5">📂 Standalone File on your Computer:</span>
            <span class="font-mono text-[11px] text-cyan-400 truncate block">c:\\Users\\user\\Desktop\\Uni\\gin400\\chapter1.html</span>
          </div>
          <span class="shrink-0 text-[10px] bg-slate-800 px-2 py-1 rounded text-slate-300 font-mono">Offline Ready</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Recording In-Progress Banner -->
  <div id="recordingBanner" class="fixed top-4 right-4 z-50 bg-red-950/95 border border-red-500 text-white px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-3 hidden animate-pulse">
    <span class="w-3 h-3 rounded-full bg-red-500 animate-ping"></span>
    <span id="recordingText" class="font-bold text-xs font-mono">RECORDING IN PROGRESS...</span>
    <button id="cancelRecordBtn" class="text-slate-300 hover:text-white font-bold text-xs ml-2 bg-red-900/80 hover:bg-red-800 px-2.5 py-1 rounded transition">STOP & SAVE</button>
  </div>

  <!-- Interactive Sandbox Modal -->
  <div id="sandboxModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full p-6 shadow-2xl flex flex-col gap-4 max-h-[90vh] overflow-y-auto custom-scroll">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-2xl">🧮</span>
          <div>
            <h3 class="font-bold text-white text-lg">Interactive Physical Storage & Index Sandbox</h3>
            <p class="text-xs text-slate-400">Simulate Disk Latency, Blocking Factor, Multi-Level Fanout & Bitmap Evaluation</p>
          </div>
        </div>
        <button id="closeSandboxBtn" class="text-slate-400 hover:text-white text-2xl font-bold">&times;</button>
      </div>

      <!-- Simulator 1: Disk Latency & Transfer -->
      <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-4">
        <h4 class="font-semibold text-cyan-400 text-sm flex items-center gap-2">
          <span>💽</span> 1. Magnetic Disk Access Latency Simulator
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div>
            <label class="block text-slate-300 mb-1">Rotational Speed (RPM): <span id="valRpm" class="font-mono text-cyan-400 font-bold">7200</span></label>
            <input id="inputRpm" type="range" min="3600" max="15000" step="600" value="7200" class="w-full accent-cyan-500">
          </div>
          <div>
            <label class="block text-slate-300 mb-1">Avg Seek Time ($s$): <span id="valSeek" class="font-mono text-cyan-400 font-bold">8.0 ms</span></label>
            <input id="inputSeek" type="range" min="1" max="20" step="0.5" value="8" class="w-full accent-cyan-500">
          </div>
          <div>
            <label class="block text-slate-300 mb-1">Transfer Rate: <span id="valTransfer" class="font-mono text-cyan-400 font-bold">100 MB/s</span></label>
            <input id="inputTransfer" type="range" min="20" max="500" step="10" value="100" class="w-full accent-cyan-500">
          </div>
        </div>

        <div class="bg-slate-900 rounded-lg p-3 grid grid-cols-2 md:grid-cols-4 gap-2 text-center text-xs border border-slate-800 font-mono">
          <div>
            <span class="text-slate-400 block text-[10px]">Rotational Delay ($r/2$)</span>
            <span id="resRotDelay" class="text-cyan-400 font-bold text-base">4.17 ms</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">Block Transfer (4KB)</span>
            <span id="resTransTime" class="text-cyan-400 font-bold text-base">0.04 ms</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">Total Block Latency</span>
            <span id="resTotalLatency" class="text-amber-400 font-bold text-base">12.21 ms</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">IOPS (Random 4KB)</span>
            <span id="resIops" class="text-emerald-400 font-bold text-base">82 IOPS</span>
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-3 text-center my-2">
          <span class="text-[11px] text-cyan-400 block mb-1 uppercase tracking-wider font-mono font-bold">Latency Derivation Formula</span>
          <div id="sandboxLatencyFormula" class="text-sm md:text-base text-yellow-300 font-serif py-1 overflow-x-auto">
            <!-- Rendered dynamically via KaTeX -->
          </div>
        </div>
      </div>

      <!-- Simulator 2: Blocking Factor & Multi-Level Index Fanout -->
      <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-4">
        <h4 class="font-semibold text-blue-400 text-sm flex items-center gap-2">
          <span>📦</span> 2. Blocking Factor & B+ Tree Height Calculator
        </h4>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div>
            <label class="block text-slate-300 mb-1">Records ($r$):</label>
            <input id="inputRecs" type="number" value="100000" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-white font-mono">
          </div>
          <div>
            <label class="block text-slate-300 mb-1">Record Size ($R$ bytes):</label>
            <input id="inputRecSize" type="number" value="200" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-white font-mono">
          </div>
          <div>
            <label class="block text-slate-300 mb-1">Block Size ($B$ bytes):</label>
            <input id="inputBlockSize" type="number" value="4096" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-white font-mono">
          </div>
          <div>
            <label class="block text-slate-300 mb-1">Index Entry ($V+P$):</label>
            <input id="inputIndexEntry" type="number" value="16" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-white font-mono">
          </div>
        </div>

        <div class="bg-slate-900 rounded-lg p-3 grid grid-cols-2 md:grid-cols-5 gap-2 text-center text-xs border border-slate-800 font-mono">
          <div>
            <span class="text-slate-400 block text-[10px]">Data $bfr$</span>
            <span id="resBfr" class="text-blue-400 font-bold text-sm">20 recs/blk</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">Data Blocks ($b$)</span>
            <span id="resDataBlocks" class="text-blue-400 font-bold text-sm">5,000</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">Index Fanout ($fo$)</span>
            <span id="resFanout" class="text-indigo-400 font-bold text-sm">256</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">Primary Idx Blks ($b_I$)</span>
            <span id="resIndexBlocks" class="text-emerald-400 font-bold text-sm">20</span>
          </div>
          <div>
            <span class="text-slate-400 block text-[10px]">B+ Tree Height ($x$)</span>
            <span id="resTreeHeight" class="text-yellow-400 font-bold text-sm">2 levels</span>
          </div>
        </div>

        <!-- Search Cost Comparison -->
        <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800 text-xs">
          <span class="text-[11px] font-bold text-cyan-400 block mb-2 uppercase font-mono">Access Strategy Showdown for finding 1 Record:</span>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-center">
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 block text-[10px]">Heap File (Avg)</span>
              <span id="resHeapCost" class="text-red-400 font-bold font-mono">2,500 I/Os</span>
            </div>
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 block text-[10px]">Binary Search</span>
              <span id="resBinCost" class="text-amber-400 font-bold font-mono">13 I/Os</span>
            </div>
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 block text-[10px]">Primary Index</span>
              <span id="resPrimCost" class="text-blue-400 font-bold font-mono">6 I/Os</span>
            </div>
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 block text-[10px]">B+ Tree (Optimal)</span>
              <span id="resBTreeCost" class="text-emerald-400 font-bold font-mono">3 I/Os</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Audio Payload, Subtitle Timings & Application Script -->
  <script>
    const AUDIO_TRACKS = """ + json.dumps(audio_tracks) + """;
    const AUDIO_DURATIONS = """ + json.dumps(audio_durations) + """;
    const SUBTITLES_DATA = """ + json.dumps(subtitles_data) + """;

    // --- Dynamic Spotlight Highlighter Helper ---
    function drawSpotlightHighlight(ctx, x, y, w, h, color = "#38bdf8", label = "NOW DISCUSSING", t = 0) {
      ctx.save();
      const glow = 18 + 8 * Math.sin(t * 8);
      ctx.shadowColor = color;
      ctx.shadowBlur = glow;
      ctx.strokeStyle = color;
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.roundRect(x - 5, y - 5, w + 10, h + 10, 14);
      ctx.stroke();

      // Floating Badge
      ctx.shadowBlur = 10;
      ctx.fillStyle = color;
      const bw = Math.min(220, label.length * 7.5 + 40);
      const bx = Math.max(x + 10, x + w - bw - 10);
      ctx.beginPath();
      ctx.roundRect(bx, y - 18, bw, 24, 6);
      ctx.fill();

      ctx.shadowBlur = 0;
      ctx.fillStyle = "#020617";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("🎙️ " + label, bx + bw / 2, y - 2);
      ctx.restore();
    }

    function drawBackgroundGrid(ctx, w, h) {
      ctx.fillStyle = "#030712";
      ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = "rgba(14, 165, 233, 0.07)";
      ctx.lineWidth = 1;
      const step = 40;
      ctx.beginPath();
      for (let x = 0; x < w; x += step) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
      }
      for (let y = 0; y < h; y += step) {
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
      }
      ctx.stroke();
    }

    // 6 Masterclass Scenes for Chapter 1
    const scenes = [
      {
        id: 0,
        title: "1. Physical Storage Hierarchy & Disk Geometry",
        duration: AUDIO_DURATIONS[0],
        icon: "💽",
        summary: "Magnetic disk pack architecture: rotating platters, concentric tracks, cylinder alignment, and sector subdivisions. Physical block addressing via $(\\\\text{Surface}, \\\\text{Track}, \\\\text{Sector})$. Mechanical delay breakdown: Seek Time $s$, Rotational Latency $r/2$, and Transfer Time $b/t$. Double buffering and RAID striping concurrency.",
        hudCost: "\\\\text{Address} = (\\\\text{Surface}, \\\\text{Track}, \\\\text{Sector})",
        audioUri: AUDIO_TRACKS[0],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          // Left Half: Animated Spinning Magnetic Platter & Actuator Arm
          const cx = 340;
          const cy = h / 2 + 10;
          const maxR = 190;

          // Platter Base Shadow & Rim
          ctx.save();
          ctx.shadowColor = "rgba(6, 182, 212, 0.35)";
          ctx.shadowBlur = 30;
          ctx.fillStyle = "#082f49";
          ctx.beginPath();
          ctx.arc(cx, cy, maxR + 10, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();

          // Concentric Tracks (Outer, Middle, Inner)
          const trackRadii = [maxR, maxR * 0.78, maxR * 0.56, maxR * 0.34];
          const trackColors = ["#0284c7", "#0ea5e9", "#38bdf8", "#7dd3fc"];

          trackRadii.forEach((r, idx) => {
            ctx.strokeStyle = trackColors[idx];
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.arc(cx, cy, r, 0, Math.PI * 2);
            ctx.stroke();
          });

          // Spinning Sectors (8 Slices)
          const rotAngle = t * 1.8;
          ctx.save();
          ctx.translate(cx, cy);
          ctx.rotate(rotAngle);

          for (let i = 0; i < 8; i++) {
            const angle = (i * Math.PI) / 4;
            ctx.strokeStyle = "rgba(255, 255, 255, 0.18)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(Math.cos(angle) * maxR, Math.sin(angle) * maxR);
            ctx.stroke();

            // Highlight target sector with neon glow
            if (i === 2) {
              ctx.fillStyle = "rgba(6, 182, 212, 0.3)";
              ctx.beginPath();
              ctx.moveTo(0, 0);
              ctx.arc(0, 0, maxR * 0.78, angle, angle + Math.PI / 4);
              ctx.closePath();
              ctx.fill();
            }
          }

          // Center Spindle
          ctx.fillStyle = "#1e293b";
          ctx.strokeStyle = "#06b6d4";
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(0, 0, 36, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 10px monospace";
          ctx.textAlign = "center";
          ctx.fillText("SPINDLE", 0, 4);
          ctx.restore();

          // Movable Actuator Arm & Read/Write Head
          const armAngle = -0.35 + 0.18 * Math.sin(t * 1.2);
          const pivotX = 110;
          const pivotY = cy - 140;
          const armLen = 270;
          const headX = pivotX + Math.cos(armAngle) * armLen;
          const headY = pivotY + Math.sin(armAngle) * armLen;

          // Arm body
          ctx.strokeStyle = "#94a3b8";
          ctx.lineWidth = 6;
          ctx.beginPath();
          ctx.moveTo(pivotX, pivotY);
          ctx.lineTo(headX, headY);
          ctx.stroke();

          // Actuator Pivot
          ctx.fillStyle = "#334155";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(pivotX, pivotY, 20, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 9px monospace";
          ctx.textAlign = "center";
          ctx.fillText("PIVOT", pivotX, pivotY + 3);

          // Head with Spark / Read Beam
          ctx.fillStyle = "#f59e0b";
          ctx.shadowColor = "#f59e0b";
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.arc(headX, headY, 9, 0, Math.PI * 2);
          ctx.fill();
          ctx.shadowBlur = 0;

          // Track label
          ctx.fillStyle = "#7dd3fc";
          ctx.font = "bold 12px monospace";
          ctx.textAlign = "center";
          ctx.fillText("CYLINDER / TRACKS", cx, cy + maxR + 32);

          // Right Half: Architectural Breakdown & Latency HUD Cards
          const rx = 650;
          const rw = 570;

          // Card 1: 3-Part Address
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#0284c7";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rx, 40, rw, 100, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 14px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("1. Physical Disk Block Addressing", rx + 20, 70);

          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 18px monospace";
          ctx.fillText("Address = ( Surface #, Track #, Sector # )", rx + 20, 105);

          ctx.fillStyle = "#94a3b8";
          ctx.font = "12px sans-serif";
          ctx.fillText("Cylinder = all tracks at identical radius across all recording surfaces.", rx + 20, 128);

          // Card 2: Latency Formula Components
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rx, 160, rw, 270, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#facc15";
          ctx.font = "bold 15px sans-serif";
          ctx.fillText("2. Physical Access Time Breakdown", rx + 20, 190);

          const latencies = [
            { name: "Seek Time (s)", val: "2 - 10 ms", desc: "Mechanical arm motion to position head on target cylinder", col: "#f87171" },
            { name: "Rotational Delay (r/2)", val: "2 - 6 ms", desc: "Platter spin time until target sector reaches head (60000 / (2 * RPM))", col: "#fbbf24" },
            { name: "Transfer Time (b/t)", val: "0.02 - 0.1 ms", desc: "Electronic bit transfer off magnetic surface (Block Size / Transfer Rate)", col: "#34d399" }
          ];

          latencies.forEach((lat, idx) => {
            const ly = 225 + idx * 60;
            ctx.fillStyle = lat.col;
            ctx.font = "bold 13px monospace";
            ctx.fillText(lat.name + ": " + lat.val, rx + 20, ly);
            ctx.fillStyle = "#cbd5e1";
            ctx.font = "11px sans-serif";
            ctx.fillText(lat.desc, rx + 20, ly + 20);
          });

          // Formula box inside Card 2
          ctx.fillStyle = "#020617";
          ctx.strokeStyle = "#facc15";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(rx + 20, 360, rw - 40, 50, 8);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#fde047";
          ctx.font = "bold 15px serif";
          ctx.textAlign = "center";
          ctx.fillText("Total Latency:  T = s + (r / 2) + (b / t)", rx + rw / 2, 390);

          // Card 3: Double Buffering & RAID Striping
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rx, 450, rw, 210, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#34d399";
          ctx.font = "bold 14px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("3. I/O Acceleration: Double Buffering & RAID Striping", rx + 20, 480);

          // Animated Double Buffering visualization
          const bufW = 220;
          const bufH = 45;
          const bufY = 505;

          // Buffer A
          ctx.fillStyle = "#064e3b";
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(rx + 20, bufY, bufW, bufH, 8);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#a7f3d0";
          ctx.font = "bold 12px sans-serif";
          ctx.fillText("Buffer A: [CPU Processing]", rx + 30, bufY + 28);

          // Buffer B
          ctx.fillStyle = "#1e3a8a";
          ctx.strokeStyle = "#38bdf8";
          ctx.beginPath();
          ctx.roundRect(rx + 280, bufY, bufW, bufH, 8);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#bae6fd";
          ctx.fillText("Buffer B: [Disk DMA Fetching]", rx + 290, bufY + 28);

          // Pulse transfer particle
          const pProg = (t * 1.5) % 1;
          ctx.fillStyle = "#facc15";
          ctx.beginPath();
          ctx.arc(rx + 240 + pProg * 40, bufY + bufH / 2, 5, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = "#94a3b8";
          ctx.font = "11px sans-serif";
          ctx.fillText("Concurrency: CPU processes Buffer A while Disk Controller fills Buffer B.", rx + 20, 580);
          ctx.fillText("RAID 0/5 Striping distributes blocks across independent arms to multiply bandwidth.", rx + 20, 600);

          // Active Voice Spotlight Calibration
          if (t >= 0 && t < 14) {
            drawSpotlightHighlight(ctx, 40, 60, 580, 560, "#0ea5e9", "SECONDARY STORAGE & DISK PACK", t);
            updateHUDTopic("Physical Disk Assembly");
          } else if (t >= 14 && t < 28) {
            drawSpotlightHighlight(ctx, rx, 40, rw, 100, "#38bdf8", "CYLINDERS & 3-PART ADDRESSING", t);
            updateHUDTopic("Block Address (S, T, S)");
          } else if (t >= 28 && t < 48) {
            drawSpotlightHighlight(ctx, rx, 160, rw, 270, "#facc15", "MECHANICAL ACCESS LATENCY", t);
            updateHUDTopic("Latency s + r/2 + b/t");
          } else {
            drawSpotlightHighlight(ctx, rx, 450, rw, 210, "#34d399", "DOUBLE BUFFERING & RAID", t);
            updateHUDTopic("Double Buffering & RAID");
          }
        }
      },
      {
        id: 1,
        title: "2. Record Organization, Blocking Factor & Spanning",
        duration: AUDIO_DURATIONS[1],
        icon: "📦",
        summary: "Database files consist of records of size $R$ packed inside disk blocks of size $B$. Blocking Factor $\\\\text{bfr} = \\\\lfloor B / R \\\\rfloor$ and file blocks $b = \\\\lceil r / \\\\text{bfr} \\\\rceil$. Architectural trade-off: Unspanned records (internal fragmentation remainder $B \\\\pmod R$) versus Spanned records (zero wasted space with continuation pointers). Search costs: Heap scan ($b/2$) vs Sequential Binary Search ($\\\\lceil \\\\log_2 b \\\\rceil$).",
        hudCost: "bfr = \\\\lfloor B / R \\\\rfloor \\\\mid b = \\\\lceil r / bfr \\\\rceil",
        audioUri: AUDIO_TRACKS[1],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          // Top Header Summary
          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 20px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Record Layout: Unspanned vs Spanned Organization", 50, 45);

          // Top Formula Bar
          const fboxW = w - 100;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#0ea5e9";
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.roundRect(50, 65, fboxW, 70, 10);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 13px monospace";
          ctx.fillText("CORE PARAMETERS:", 70, 92);
          ctx.fillStyle = "#fde047";
          ctx.font = "bold 15px serif";
          ctx.fillText("Blocking Factor:  bfr = \\u230A B / R \\u230B       Total File Blocks:  b = \\u2308 r / bfr \\u2309       Wasted / Block:  W = B mod R", 70, 118);

          // Middle Containers: Side-by-Side Comparison
          const colW = (w - 130) / 2;
          const colH = 340;
          const colY = 155;

          // Left Box: Unspanned
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(50, colY, colW, colH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 16px sans-serif";
          ctx.fillText("A. Unspanned Organization (Standard)", 75, colY + 35);
          ctx.fillStyle = "#94a3b8";
          ctx.font = "12px sans-serif";
          ctx.fillText("Each record is entirely self-contained inside one disk block.", 75, colY + 60);

          // Visual representation of Block with Slots
          const blkX = 75;
          const blkY = colY + 80;
          const blkW = colW - 50;
          const blkH = 110;

          ctx.fillStyle = "#1e293b";
          ctx.strokeStyle = "#64748b";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(blkX, blkY, blkW, blkH, 8);
          ctx.fill();
          ctx.stroke();

          // Record Slots R1, R2, R3, R4
          const slotW = (blkW - 60) / 3;
          for (let i = 0; i < 3; i++) {
            ctx.fillStyle = "#0369a1";
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.roundRect(blkX + 10 + i * (slotW + 6), blkY + 15, slotW, blkH - 30, 6);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 13px monospace";
            ctx.textAlign = "center";
            ctx.fillText("Rec " + (i + 1), blkX + 10 + i * (slotW + 6) + slotW / 2, blkY + 55);
            ctx.font = "10px sans-serif";
            ctx.fillStyle = "#bae6fd";
            ctx.fillText("R bytes", blkX + 10 + i * (slotW + 6) + slotW / 2, blkY + 72);
          }

          // Wasted Fragmentation Remainder
          const fragX = blkX + 10 + 3 * (slotW + 6);
          const fragW = blkW - fragX + blkX - 10;
          ctx.fillStyle = "#7f1d1d";
          ctx.strokeStyle = "#ef4444";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(fragX, blkY + 15, fragW, blkH - 30, 6);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#fca5a5";
          ctx.font = "bold 11px monospace";
          ctx.textAlign = "center";
          ctx.fillText("WASTE", fragX + fragW / 2, blkY + 50);
          ctx.font = "9px monospace";
          ctx.fillText("W = B mod R", fragX + fragW / 2, blkY + 68);

          // Details List
          ctx.textAlign = "left";
          ctx.fillStyle = "#cbd5e1";
          ctx.font = "12px sans-serif";
          ctx.fillText("✔ Record never crosses block boundary", 75, colY + 225);
          ctx.fillText("✔ Exactly 1 block I/O per record read", 75, colY + 250);
          ctx.fillStyle = "#f87171";
          ctx.fillText("✖ Leaves unused leftover bytes (Internal Fragmentation)", 75, colY + 275);
          ctx.fillText("✖ Cannot store records where record size R > block size B", 75, colY + 300);

          // Right Box: Spanned
          const rightX = 50 + colW + 30;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rightX, colY, colW, colH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#34d399";
          ctx.font = "bold 16px sans-serif";
          ctx.fillText("B. Spanned Organization (Continuation Pointers)", rightX + 25, colY + 35);
          ctx.fillStyle = "#94a3b8";
          ctx.font = "12px sans-serif";
          ctx.fillText("Large records cross boundary into the consecutive block.", rightX + 25, colY + 60);

          // Visual representation of Block i and Block i+1
          const spBlkW = (colW - 70) / 2;
          // Block i
          ctx.fillStyle = "#1e293b";
          ctx.strokeStyle = "#64748b";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rightX + 25, blkY, spBlkW, blkH, 8);
          ctx.fill();
          ctx.stroke();

          // Block i+1
          ctx.beginPath();
          ctx.roundRect(rightX + 45 + spBlkW, blkY, spBlkW, blkH, 8);
          ctx.fill();
          ctx.stroke();

          // Spanned Record Segment 1
          ctx.fillStyle = "#047857";
          ctx.strokeStyle = "#34d399";
          ctx.beginPath();
          ctx.roundRect(rightX + 25 + spBlkW - 55, blkY + 15, 45, blkH - 30, 4);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 9px monospace";
          ctx.textAlign = "center";
          ctx.fillText("R3 pt.1", rightX + 25 + spBlkW - 32, blkY + 55);

          // Pointer Arrow between blocks
          ctx.strokeStyle = "#facc15";
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(rightX + 25 + spBlkW - 10, blkY + blkH / 2);
          ctx.lineTo(rightX + 45 + spBlkW + 10, blkY + blkH / 2);
          ctx.stroke();

          // Spanned Record Segment 2
          ctx.fillStyle = "#047857";
          ctx.strokeStyle = "#34d399";
          ctx.beginPath();
          ctx.roundRect(rightX + 45 + spBlkW + 15, blkY + 15, 45, blkH - 30, 4);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#ffffff";
          ctx.fillText("R3 pt.2", rightX + 45 + spBlkW + 37, blkY + 55);

          // Details List
          ctx.textAlign = "left";
          ctx.fillStyle = "#cbd5e1";
          ctx.font = "12px sans-serif";
          ctx.fillText("✔ Eliminates all internal fragmentation (W = 0)", rightX + 25, colY + 225);
          ctx.fillText("✔ Permits records larger than a single block (R > B)", rightX + 25, colY + 250);
          ctx.fillStyle = "#f87171";
          ctx.fillText("✖ Spanned records require 2 disk block fetches to read", rightX + 25, colY + 275);
          ctx.fillText("✖ Pointer maintenance overhead during updates & deletes", rightX + 25, colY + 300);

          // Bottom Access Cost Comparison
          const botY = 515;
          const botH = 150;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#f59e0b";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(50, botY, fboxW, botH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#fbbf24";
          ctx.font = "bold 15px sans-serif";
          ctx.fillText("Search Cost Benchmark: Unordered Heap vs Sequential Binary Search", 75, botY + 35);

          const heapCost = "Average = b / 2 Block Transfers   |   Worst-Case = b Block Transfers";
          const binCost = "Cost = \\u2308 log\\u2082(b) \\u2309 Block Transfers";

          ctx.fillStyle = "#ef4444";
          ctx.font = "bold 13px monospace";
          ctx.fillText("1. Heap File (Unordered Scan):", 75, botY + 70);
          ctx.fillStyle = "#ffffff";
          ctx.fillText(heapCost, 350, botY + 70);

          ctx.fillStyle = "#10b981";
          ctx.fillText("2. Ordered File (Binary Search):", 75, botY + 105);
          ctx.fillStyle = "#fde047";
          ctx.fillText(binCost + "    (e.g., b = 1,000 blks \\u27F9 \\u2308log\\u2082 1000\\u2309 = 10 I/Os vs 500 I/Os!)", 350, botY + 105);

          // Voice Spotlight Calibration
          if (t >= 0 && t < 15) {
            drawSpotlightHighlight(ctx, 50, 65, fboxW, 70, "#0ea5e9", "BLOCKING FACTOR bfr = \u230AB/R\u230B", t);
            updateHUDTopic("Blocking Factor bfr");
          } else if (t >= 15 && t < 37) {
            drawSpotlightHighlight(ctx, 50, colY, colW, colH, "#38bdf8", "UNSPANNED & INTERNAL FRAGMENTATION", t);
            updateHUDTopic("Unspanned Organization");
          } else if (t >= 37 && t < 50) {
            drawSpotlightHighlight(ctx, rightX, colY, colW, colH, "#34d399", "SPANNED & CONTINUATION POINTERS", t);
            updateHUDTopic("Spanned Records");
          } else {
            drawSpotlightHighlight(ctx, 50, botY, fboxW, botH, "#fbbf24", "SEARCH COST: HEAP vs BINARY", t);
            updateHUDTopic("Binary Search log2(b)");
          }
        }
      },
      {
        id: 2,
        title: "3. Single-Level Indexes: Primary, Clustering, & Secondary",
        duration: AUDIO_DURATIONS[2],
        icon: "📑",
        summary: "Single-level ordered index architectures. Primary Index: Sparse on primary key, contains 1 anchor entry per block ($r_I = b$), search cost $\\\\lceil \\\\log_2 b_I \\\\rceil + 1$. Clustering Index: Sparse on non-key ordering field, 1 entry per distinct value ($r_I = d$). Secondary Index: Dense on candidate key ($r_I = r$) or indirection pointer buckets for non-key duplicate values.",
        hudCost: "b_I = \\\\lceil b / bfr_I \\\\rceil \\\\mid \\\\text{Cost} = \\\\lceil \\\\log_2(b_I) \\\\rceil + 1",
        audioUri: AUDIO_TRACKS[2],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 20px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Single-Level Index Architectures: Primary, Clustering & Secondary", 50, 45);

          // 3 Side-by-Side Index Columns
          const cardW = (w - 140) / 3;
          const cardH = 590;
          const cardY = 75;

          const idxTypes = [
            {
              title: "1. Primary Index",
              type: "SPARSE / NON-DENSE",
              ordering: "Ordered by Primary Key",
              entries: "1 entry per Data Block (b entries)",
              dataPtr: "Block Pointer (Anchor Key)",
              cost: "\\u2308 log\\u2082(b_I) \\u2309 + 1 I/O",
              accent: "#38bdf8",
              bg: "#0c4a6e"
            },
            {
              title: "2. Clustering Index",
              type: "SPARSE / NON-DENSE",
              ordering: "Ordered by Non-Key Field",
              entries: "1 entry per Distinct Value d",
              dataPtr: "Block Pointer (1st block of cluster)",
              cost: "\\u2308 log\\u2082(b_I) \\u2309 + cluster blks",
              accent: "#a855f7",
              bg: "#581c87"
            },
            {
              title: "3. Secondary Index",
              type: "DENSE or INDIRECTION",
              ordering: "Non-Ordering Field",
              entries: "Candidate Key: r entries (Dense)",
              dataPtr: "Record Pointer <Block, Slot>",
              cost: "\\u2308 log\\u2082(b_I) \\u2309 + 1 I/O (Key)",
              accent: "#10b981",
              bg: "#064e3b"
            }
          ];

          idxTypes.forEach((it, idx) => {
            const ix = 50 + idx * (cardW + 20);

            ctx.fillStyle = "#0f172a";
            ctx.strokeStyle = it.accent;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(ix, cardY, cardW, cardH, 12);
            ctx.fill();
            ctx.stroke();

            // Header Tag
            ctx.fillStyle = it.accent;
            ctx.font = "bold 16px sans-serif";
            ctx.textAlign = "left";
            ctx.fillText(it.title, ix + 18, cardY + 32);

            ctx.fillStyle = it.bg;
            ctx.beginPath();
            ctx.roundRect(ix + 18, cardY + 45, cardW - 36, 26, 6);
            ctx.fill();
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 11px monospace";
            ctx.textAlign = "center";
            ctx.fillText(it.type, ix + cardW / 2, cardY + 62);

            // Visual Index diagram inside card
            const diagY = cardY + 85;
            const diagH = 210;
            ctx.fillStyle = "#020617";
            ctx.strokeStyle = "#334155";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.roundRect(ix + 18, diagY, cardW - 36, diagH, 8);
            ctx.fill();
            ctx.stroke();

            // Draw mini index table vs data blocks
            const itblX = ix + 28;
            const dtblX = ix + cardW - 130;

            // Index entries
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = it.accent;
            ctx.lineWidth = 1;
            for (let r = 0; r < 4; r++) {
              const ey = diagY + 20 + r * 44;
              ctx.strokeRect(itblX, ey, 75, 34);
              ctx.fillStyle = "#cbd5e1";
              ctx.font = "9px monospace";
              ctx.textAlign = "center";
              ctx.fillText("K" + (r * 10 + 1) + " | \\u2192", itblX + 37, ey + 21);

              // Data blocks
              ctx.fillStyle = "#1e293b";
              ctx.strokeStyle = "#64748b";
              ctx.strokeRect(dtblX, ey, 80, 34);
              ctx.fillStyle = "#94a3b8";
              ctx.fillText("Blk #" + (r + 1), dtblX + 40, ey + 21);

              // Pointer lines with animated dot
              ctx.strokeStyle = it.accent;
              ctx.lineWidth = 1.5;
              ctx.beginPath();
              ctx.moveTo(itblX + 75, ey + 17);
              ctx.lineTo(dtblX, ey + 17);
              ctx.stroke();

              const pProg = (t * 1.5 + r * 0.25) % 1;
              ctx.fillStyle = "#facc15";
              ctx.beginPath();
              ctx.arc(itblX + 75 + pProg * (dtblX - itblX - 75), ey + 17, 3, 0, Math.PI * 2);
              ctx.fill();
            }

            // Specs text
            ctx.textAlign = "left";
            const ty = diagY + diagH + 30;
            ctx.fillStyle = "#94a3b8";
            ctx.font = "11px sans-serif";
            ctx.fillText("Ordering Field:", ix + 18, ty);
            ctx.fillStyle = "#e2e8f0";
            ctx.font = "bold 12px sans-serif";
            ctx.fillText(it.ordering, ix + 18, ty + 18);

            ctx.fillStyle = "#94a3b8";
            ctx.font = "11px sans-serif";
            ctx.fillText("Index Entries Count:", ix + 18, ty + 46);
            ctx.fillStyle = "#38bdf8";
            ctx.font = "bold 12px monospace";
            ctx.fillText(it.entries, ix + 18, ty + 64);

            ctx.fillStyle = "#94a3b8";
            ctx.font = "11px sans-serif";
            ctx.fillText("Pointer Target:", ix + 18, ty + 92);
            ctx.fillStyle = "#cbd5e1";
            ctx.font = "bold 12px sans-serif";
            ctx.fillText(it.dataPtr, ix + 18, ty + 110);

            // Cost Box
            ctx.fillStyle = "#020617";
            ctx.strokeStyle = it.accent;
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.roundRect(ix + 18, ty + 140, cardW - 36, 50, 8);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = "#facc15";
            ctx.font = "bold 13px monospace";
            ctx.textAlign = "center";
            ctx.fillText("Access Cost:", ix + cardW / 2, ty + 160);
            ctx.fillStyle = "#ffffff";
            ctx.fillText(it.cost, ix + cardW / 2, ty + 178);
          });

          // Voice Spotlight Calibration
          if (t >= 0 && t < 12) {
            updateHUDTopic("Single-Level Indexing");
          } else if (t >= 12 && t < 28) {
            drawSpotlightHighlight(ctx, 50, cardY, cardW, cardH, "#38bdf8", "PRIMARY INDEX (SPARSE)", t);
            updateHUDTopic("Primary Index (Anchor)");
          } else if (t >= 28 && t < 43) {
            drawSpotlightHighlight(ctx, 50 + cardW + 20, cardY, cardW, cardH, "#a855f7", "CLUSTERING INDEX (DISTINCT d)", t);
            updateHUDTopic("Clustering Index (d values)");
          } else {
            drawSpotlightHighlight(ctx, 50 + (cardW + 20) * 2, cardY, cardW, cardH, "#10b981", "SECONDARY INDEX (INDIRECTION)", t);
            updateHUDTopic("Secondary Indirection");
          }
        }
      },
      {
        id: 3,
        title: "4. Multi-Level Indexing & B+ Tree Architecture",
        duration: AUDIO_DURATIONS[3],
        icon: "🌲",
        summary: "Multi-level indexing reduces the search space by the index fanout $fo = \\\\text{bfr}_I$ at each tier. Tree height $x = \\\\lceil \\\\log_{fo}(b_{i1}) \\\\rceil + 1$. B-Tree vs B+-Tree architecture: B-Trees keep record pointers across all levels, while B+-Trees push all record pointers to leaf blocks linked into a doubly linked list, enabling both point queries in 3-4 I/Os and high-speed range scans.",
        hudCost: "t = x = \\\\lceil \\\\log_{fo}(b_{i1}) \\\\rceil + 1 \\\\mid fo = bfr_I",
        audioUri: AUDIO_TRACKS[3],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 20px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Multi-Level Balanced Indexing: B+ Tree Architecture", 50, 45);

          // Top Formula Card
          const fboxW = w - 100;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.roundRect(50, 65, fboxW, 60, 10);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#34d399";
          ctx.font = "bold 13px monospace";
          ctx.fillText("FANOUT & HEIGHT:", 70, 90);
          ctx.fillStyle = "#fde047";
          ctx.font = "bold 14px serif";
          ctx.fillText("Fanout:  fo = bfr_I = \\u230A B / (V + P) \\u230B       Height:  x = \\u2308 log_fo(b_i1) \\u2309 + 1       Lookup Cost:  x + 1 Data Block I/O", 70, 110);

          // B+ Tree Graphical Hierarchy
          // Level 1: Root Node
          const rootX = w / 2 - 120;
          const rootY = 150;
          const rootW = 240;
          const rootH = 50;

          ctx.fillStyle = "#1e1b4b";
          ctx.strokeStyle = "#818cf8";
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.roundRect(rootX, rootY, rootW, rootH, 10);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 14px monospace";
          ctx.textAlign = "center";
          ctx.fillText("Root: [ P1 | 30 | P2 | 70 | P3 ]", rootX + rootW / 2, rootY + 30);

          // Level 2: Internal Nodes (3 children)
          const midY = 270;
          const midW = 190;
          const midH = 45;
          const midPositions = [140, w / 2 - midW / 2, w - 140 - midW];

          midPositions.forEach((mx, idx) => {
            // Branch pointer line from root
            ctx.strokeStyle = "#6366f1";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(rootX + 40 + idx * 80, rootY + rootH);
            ctx.lineTo(mx + midW / 2, midY);
            ctx.stroke();

            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(mx, midY, midW, midH, 8);
            ctx.fill();
            ctx.stroke();

            const lbls = ["P1 | 15 | P2", "P3 | 45 | P4", "P5 | 85 | P6"];
            ctx.fillStyle = "#c7d2fe";
            ctx.font = "bold 12px monospace";
            ctx.textAlign = "center";
            ctx.fillText("Int " + (idx + 1) + ": [ " + lbls[idx] + " ]", mx + midW / 2, midY + 28);
          });

          // Level 3: Leaf Nodes (6 leaf blocks connected via doubly linked list)
          const leafY = 400;
          const leafW = 160;
          const leafH = 50;
          const leafSpacing = (w - 120 - 6 * leafW) / 5;

          const leafKeys = [
            "[5, 10, 15]",
            "[20, 25, 30]",
            "[35, 40, 45]",
            "[50, 60, 70]",
            "[75, 80, 85]",
            "[90, 95, 99]"
          ];

          for (let i = 0; i < 6; i++) {
            const lx = 60 + i * (leafW + leafSpacing);

            // Parent link from internal node
            const parentIdx = Math.floor(i / 2);
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(midPositions[parentIdx] + 45 + (i % 2) * 100, midY + midH);
            ctx.lineTo(lx + leafW / 2, leafY);
            ctx.stroke();

            // Leaf block
            ctx.fillStyle = "#064e3b";
            ctx.strokeStyle = "#10b981";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(lx, leafY, leafW, leafH, 8);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = "#6ee7b7";
            ctx.font = "bold 11px monospace";
            ctx.textAlign = "center";
            ctx.fillText("Leaf " + (i + 1) + ": " + leafKeys[i], lx + leafW / 2, leafY + 30);

            // Doubly Linked Sibling Pointers (Green Horizontal Arrows)
            if (i < 5) {
              const nextLx = 60 + (i + 1) * (leafW + leafSpacing);
              ctx.strokeStyle = "#34d399";
              ctx.lineWidth = 2.5;
              ctx.beginPath();
              ctx.moveTo(lx + leafW, leafY + leafH / 2);
              ctx.lineTo(nextLx, leafY + leafH / 2);
              ctx.stroke();

              // Arrow head
              ctx.fillStyle = "#34d399";
              ctx.beginPath();
              ctx.moveTo(nextLx - 5, leafY + leafH / 2 - 4);
              ctx.lineTo(nextLx, leafY + leafH / 2);
              ctx.lineTo(nextLx - 5, leafY + leafH / 2 + 4);
              ctx.fill();
            }
          }

          // Leaf Pointer Label
          ctx.fillStyle = "#34d399";
          ctx.font = "bold 13px sans-serif";
          ctx.textAlign = "center";
          ctx.fillText("↔ Doubly-Linked List: Ultra-Fast Range Scans (BETWEEN 20 AND 80) Without Visiting Tree Root!", w / 2, leafY + 80);

          // Animated Search Key Traversal (Searching for Key = 42)
          const travProg = (t * 0.8) % 3;
          let travX = rootX + rootW / 2;
          let travY = rootY + 25;
          let travText = "Search Key = 42";

          if (travProg < 1) {
            travX = rootX + 140;
            travY = rootY + 25;
          } else if (travProg < 2) {
            travX = midPositions[1] + midW / 2;
            travY = midY + 25;
          } else {
            travX = 60 + 2 * (leafW + leafSpacing) + leafW / 2;
            travY = leafY + 25;
            travText = "Key 42 Found! -> Fetch Data Block";
          }

          ctx.fillStyle = "#facc15";
          ctx.shadowColor = "#facc15";
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.arc(travX, travY, 8, 0, Math.PI * 2);
          ctx.fill();
          ctx.shadowBlur = 0;

          // Bottom Comparison Table: B-Tree vs B+ Tree
          const botY = 515;
          const botH = 160;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#6366f1";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(50, botY, fboxW, botH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#818cf8";
          ctx.font = "bold 15px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("B-Tree vs B+ Tree Production Comparison", 75, botY + 30);

          ctx.fillStyle = "#cbd5e1";
          ctx.font = "12px sans-serif";
          ctx.fillText("• Standard B-Tree: Record pointers stored at all internal nodes. Lower fanout \\u27F9 deeper tree, slower searches.", 75, botY + 60);
          ctx.fillText("• B+ Tree: Data pointers reside EXCLUSIVELY in leaf nodes. Internal nodes hold only routing keys.", 75, botY + 85);
          ctx.fillStyle = "#34d399";
          ctx.fillText("• Result: High Fanout (100 - 200) \\u27F9 Shallow tree (height 3-4 can index billions of tuples in 4 disk I/Os!)", 75, botY + 110);
          ctx.fillText("• Sequential leaf chain allows index range scans without backtracking up the hierarchy.", 75, botY + 135);

          // Voice Spotlight Calibration
          if (t >= 0 && t < 15) {
            drawSpotlightHighlight(ctx, 50, 65, fboxW, 60, "#34d399", "MULTI-LEVEL FANOUT ADVANTAGE", t);
            updateHUDTopic("Multi-Level Fanout");
          } else if (t >= 15 && t < 35) {
            drawSpotlightHighlight(ctx, 40, 140, w - 80, 360, "#818cf8", "B+ TREE BALANCED HIERARCHY", t);
            updateHUDTopic("B+ Tree Hierarchy");
          } else {
            drawSpotlightHighlight(ctx, 50, botY, fboxW, botH, "#10b981", "B-TREE vs B+ TREE COMPARISON", t);
            updateHUDTopic("B-Tree vs B+ Tree");
          }
        }
      },
      {
        id: 4,
        title: "5. Static vs Extendable Hashing & Dynamic Directories",
        duration: AUDIO_DURATIONS[4],
        icon: "🔑",
        summary: "Hash indexing uses hash function $h(k)$ for direct block calculation. Static Hashing flaws: fixed buckets $M$ lead to long overflow collision chains and degraded linear scans. Extendable Hashing solves this via a dynamic directory of size $2^d$ (Global Depth $d$) and bucket Local Depth $d'$. Bucket overflow splits: if $d' = d$, directory doubles ($d \\\\leftarrow d + 1$); if $d' < d$, bucket splits without doubling directory.",
        hudCost: "\\\\text{Directory} = 2^d \\\\mid d' = d \\\\implies d \\\\leftarrow d + 1",
        audioUri: AUDIO_TRACKS[4],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 20px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Dynamic Hashing: Static Pitfalls vs Extendable Hashing", 50, 45);

          // Left Half: Static Hashing Overflow Chains
          const leftW = 440;
          const leftH = 590;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#f87171";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(50, 75, leftW, leftH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#f87171";
          ctx.font = "bold 16px sans-serif";
          ctx.fillText("A. Static Hashing (Collision Pitfall)", 75, 110);
          ctx.fillStyle = "#94a3b8";
          ctx.font = "12px sans-serif";
          ctx.fillText("Fixed primary buckets M. Collisions form linked overflow chains.", 75, 135);

          // Static buckets
          for (let b = 0; b < 4; b++) {
            const by = 165 + b * 95;
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#64748b";
            ctx.lineWidth = 1.5;
            ctx.strokeRect(75, by, 110, 45);
            ctx.fillStyle = "#e2e8f0";
            ctx.font = "bold 12px monospace";
            ctx.textAlign = "center";
            ctx.fillText("Bucket " + b, 130, by + 28);

            // Overflow chain on Bucket 2
            if (b === 2) {
              ctx.strokeStyle = "#ef4444";
              ctx.lineWidth = 2;
              ctx.beginPath();
              ctx.moveTo(185, by + 22);
              ctx.lineTo(235, by + 22);
              ctx.stroke();

              // Overflow 1
              ctx.fillStyle = "#7f1d1d";
              ctx.strokeStyle = "#f87171";
              ctx.strokeRect(235, by, 90, 45);
              ctx.fillStyle = "#ffffff";
              ctx.fillText("Overflow 1", 280, by + 28);

              // Overflow 2
              ctx.strokeStyle = "#ef4444";
              ctx.beginPath();
              ctx.moveTo(325, by + 22);
              ctx.lineTo(365, by + 22);
              ctx.stroke();

              ctx.strokeRect(365, by, 90, 45);
              ctx.fillText("Overflow 2", 410, by + 28);
            }
          }

          ctx.textAlign = "left";
          ctx.fillStyle = "#fca5a5";
          ctx.font = "bold 12px sans-serif";
          ctx.fillText("✖ File growth degrades lookups into O(N) linked list scans", 75, 560);
          ctx.fillText("✖ Pre-allocating extra buckets wastes massive storage", 75, 585);

          // Right Half: Extendable Dynamic Hashing
          const rightX = 520;
          const rightW = w - rightX - 50;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(rightX, 75, rightW, leftH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 16px sans-serif";
          ctx.fillText("B. Extendable Dynamic Hashing (Directory + Local Depth)", rightX + 25, 110);

          // Global Depth Badge
          const gDepth = t >= 45 ? 3 : 2;
          ctx.fillStyle = "#0369a1";
          ctx.beginPath();
          ctx.roundRect(rightX + rightW - 190, 95, 165, 34, 8);
          ctx.fill();
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 13px monospace";
          ctx.textAlign = "center";
          ctx.fillText("Global Depth d = " + gDepth, rightX + rightW - 107, 117);

          // Directory Entries
          const dirX = rightX + 35;
          const dirY = 160;
          const dirW = 90;
          const numEntries = Math.pow(2, gDepth);
          const dirEntryH = Math.min(45, 320 / numEntries);

          ctx.fillStyle = "#7dd3fc";
          ctx.font = "bold 12px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Directory (2^d = " + numEntries + ")", dirX, 150);

          for (let e = 0; e < numEntries; e++) {
            const ey = dirY + e * (dirEntryH + 6);
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 1.5;
            ctx.strokeRect(dirX, ey, dirW, dirEntryH);

            const binStr = e.toString(2).padStart(gDepth, '0');
            ctx.fillStyle = "#fde047";
            ctx.font = "bold 11px monospace";
            ctx.textAlign = "center";
            ctx.fillText(binStr, dirX + dirW / 2, ey + dirEntryH / 2 + 4);
          }

          // Bucket Blocks on Right
          const bktX = rightX + 240;
          const bktW = 200;
          const bktH = 65;

          const buckets = [
            { id: "Bucket A", ld: gDepth === 3 ? 3 : 2, keys: "[K4, K12]", col: "#065f46" },
            { id: "Bucket B", ld: 1, keys: "[K1, K5, K9]", col: "#1e3a8a" },
            { id: "Bucket C", ld: 2, keys: "[K2, K6]", col: "#581c87" }
          ];

          buckets.forEach((bkt, idx) => {
            const by = 165 + idx * 95;
            ctx.fillStyle = bkt.col;
            ctx.strokeStyle = "#34d399";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(bktX, by, bktW, bktH, 8);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 12px monospace";
            ctx.textAlign = "left";
            ctx.fillText(bkt.id + " (d' = " + bkt.ld + ")", bktX + 15, by + 26);
            ctx.fillStyle = "#cbd5e1";
            ctx.font = "11px sans-serif";
            ctx.fillText("Keys: " + bkt.keys, bktX + 15, by + 48);

            // Connect pointer from directory to bucket
            const fromEy = dirY + idx * 30 + 15;
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(dirX + dirW, fromEy);
            ctx.lineTo(bktX, by + bktH / 2);
            ctx.stroke();
          });

          // Bottom Rules of Extendable Hashing
          const ruleY = 490;
          ctx.fillStyle = "#020617";
          ctx.strokeStyle = "#facc15";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(rightX + 20, ruleY, rightW - 40, 150, 10);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#facc15";
          ctx.font = "bold 13px monospace";
          ctx.textAlign = "left";
          ctx.fillText("SPLIT LOGIC ON BUCKET OVERFLOW:", rightX + 35, ruleY + 28);
          ctx.fillStyle = "#ffffff";
          ctx.font = "12px sans-serif";
          ctx.fillText("1. If Local Depth d' == Global Depth d:", rightX + 35, ruleY + 55);
          ctx.fillStyle = "#38bdf8";
          ctx.fillText("   \\u27F9 Directory DOUBLES in size (d \\u2190 d + 1), bucket splits, d' increments to d' + 1", rightX + 35, ruleY + 75);
          ctx.fillStyle = "#ffffff";
          ctx.fillText("2. If Local Depth d' < Global Depth d:", rightX + 35, ruleY + 105);
          ctx.fillStyle = "#34d399";
          ctx.fillText("   \\u27F9 Bucket splits WITHOUT doubling directory! Only directory pointers are updated.", rightX + 35, ruleY + 125);

          // Voice Spotlight Calibration
          if (t >= 0 && t < 15) {
            updateHUDTopic("Hash Function h(k)");
          } else if (t >= 15 && t < 30) {
            drawSpotlightHighlight(ctx, 50, 75, leftW, leftH, "#f87171", "STATIC HASHING & OVERFLOW CHAINS", t);
            updateHUDTopic("Static Overflow Pitfall");
          } else if (t >= 30 && t < 48) {
            drawSpotlightHighlight(ctx, rightX, 75, rightW, 390, "#38bdf8", "EXTENDABLE DIRECTORY & LOCAL DEPTH", t);
            updateHUDTopic("Extendable Directory");
          } else {
            drawSpotlightHighlight(ctx, rightX + 20, ruleY, rightW - 40, 150, "#facc15", "OVERFLOW SPLIT RULES", t);
            updateHUDTopic("Split Rules d' == d");
          }
        }
      },
      {
        id: 5,
        title: "6. Bitmap Indexing & Multi-Attribute Bitwise Engine",
        duration: AUDIO_DURATIONS[5],
        icon: "🎯",
        summary: "Bitmap indices provide ultra-high-speed evaluation for attributes with low distinct cardinalities (Gender, Status, Country). Each distinct value holds a bit vector with 1 bit per relation record. Multi-attribute queries evaluate directly inside CPU registers via bitwise AND, OR, NOT operations, counting matches instantly using hardware POPCNT without reading physical disk blocks.",
        hudCost: "B_1 \\\\land B_2 \\\\mid B_1 \\\\lor B_2 \\\\mid \\\\neg B_1",
        audioUri: AUDIO_TRACKS[5],
        render: (ctx, t, w, h) => {
          ctx.clearRect(0, 0, w, h);
          drawBackgroundGrid(ctx, w, h);

          ctx.fillStyle = "#e2e8f0";
          ctx.font = "bold 20px sans-serif";
          ctx.textAlign = "left";
          ctx.fillText("Bitmap Indexing & In-Register Bitwise Query Engine", 50, 45);

          // Top Header Info
          const fboxW = w - 100;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#a855f7";
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.roundRect(50, 65, fboxW, 60, 10);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#c084fc";
          ctx.font = "bold 13px monospace";
          ctx.fillText("BITWISE BOOLEAN LOGIC:", 70, 90);
          ctx.fillStyle = "#fde047";
          ctx.font = "bold 14px serif";
          ctx.fillText("Intersection:  B_A \\u2227 B_B (AND)       Union:  B_A \\u2228 B_B (OR)       Negation:  \\u00AC B_A (NOT)       Count:  POPCNT(Result)", 70, 110);

          // Left Half: Relation Records & Bit Vectors Table
          const tblX = 50;
          const tblY = 145;
          const tblW = 550;
          const tblH = 510;

          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(tblX, tblY, tblW, tblH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 15px sans-serif";
          ctx.fillText("1. Relation Tuple to Bit Vector Mapping", tblX + 20, tblY + 30);

          // Table Headers
          const headers = ["Row #", "Gender", "Status", "B_Female", "B_Married"];
          const colX = [tblX + 20, tblX + 90, tblX + 180, tblX + 290, tblX + 420];

          ctx.fillStyle = "#94a3b8";
          ctx.font = "bold 12px monospace";
          headers.forEach((hdr, i) => {
            ctx.fillText(hdr, colX[i], tblY + 65);
          });

          // Horizontal divider
          ctx.strokeStyle = "#334155";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(tblX + 20, tblY + 75);
          ctx.lineTo(tblX + tblW - 20, tblY + 75);
          ctx.stroke();

          // 8 Records Data
          const tuples = [
            { row: "R1", g: "Male", s: "Single", bf: 0, bm: 0 },
            { row: "R2", g: "Female", s: "Married", bf: 1, bm: 1 },
            { row: "R3", g: "Female", s: "Single", bf: 1, bm: 0 },
            { row: "R4", g: "Male", s: "Married", bf: 0, bm: 1 },
            { row: "R5", g: "Female", s: "Married", bf: 1, bm: 1 },
            { row: "R6", g: "Male", s: "Divorced", bf: 0, bm: 0 },
            { row: "R7", g: "Female", s: "Divorced", bf: 1, bm: 0 },
            { row: "R8", g: "Female", s: "Married", bf: 1, bm: 1 }
          ];

          tuples.forEach((tup, idx) => {
            const ry = tblY + 105 + idx * 45;

            // Highlight matches
            if (tup.bf === 1 && tup.bm === 1) {
              ctx.fillStyle = "rgba(16, 185, 129, 0.15)";
              ctx.fillRect(tblX + 15, ry - 18, tblW - 30, 36);
            }

            ctx.fillStyle = "#cbd5e1";
            ctx.font = "12px monospace";
            ctx.fillText(tup.row, colX[0], ry);
            ctx.fillText(tup.g, colX[1], ry);
            ctx.fillText(tup.s, colX[2], ry);

            // Bit Female
            ctx.fillStyle = tup.bf === 1 ? "#34d399" : "#64748b";
            ctx.font = "bold 14px monospace";
            ctx.fillText(tup.bf.toString(), colX[3] + 15, ry);

            // Bit Married
            ctx.fillStyle = tup.bm === 1 ? "#34d399" : "#64748b";
            ctx.fillText(tup.bm.toString(), colX[4] + 15, ry);
          });

          // Right Half: Live CPU Register Bitwise Engine
          const cpuX = 630;
          const cpuW = w - cpuX - 50;
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(cpuX, tblY, cpuW, tblH, 12);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#34d399";
          ctx.font = "bold 15px sans-serif";
          ctx.fillText("2. Hardware Register Query Evaluation", cpuX + 20, tblY + 30);

          ctx.fillStyle = "#facc15";
          ctx.font = "bold 13px monospace";
          ctx.fillText("Query: WHERE Gender = 'F' AND Status = 'Married'", cpuX + 20, tblY + 65);

          // Vector 1 (Female)
          ctx.fillStyle = "#38bdf8";
          ctx.font = "bold 12px monospace";
          ctx.fillText("Reg 1 (Female):   [ 0  1  1  0  1  0  1  1 ]", cpuX + 20, tblY + 115);

          // Bitwise AND Operator
          ctx.fillStyle = "#facc15";
          ctx.font = "bold 18px monospace";
          ctx.fillText("&  (Bitwise AND inside ALU)", cpuX + 20, tblY + 150);

          // Vector 2 (Married)
          ctx.fillStyle = "#a855f7";
          ctx.font = "bold 12px monospace";
          ctx.fillText("Reg 2 (Married):  [ 0  1  0  1  1  0  0  1 ]", cpuX + 20, tblY + 185);

          // Divider
          ctx.strokeStyle = "#10b981";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(cpuX + 20, tblY + 205);
          ctx.lineTo(cpuX + cpuW - 20, tblY + 205);
          ctx.stroke();

          // Result Vector
          ctx.fillStyle = "#34d399";
          ctx.font = "bold 14px monospace";
          ctx.fillText("Result Vector:    [ 0  1  0  0  1  0  0  1 ]", cpuX + 20, tblY + 235);

          // Match Badges Box
          ctx.fillStyle = "#020617";
          ctx.strokeStyle = "#34d399";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(cpuX + 20, tblY + 265, cpuW - 40, 110, 8);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = "#fde047";
          ctx.font = "bold 13px monospace";
          ctx.fillText("Instant POPCNT = 3 Tuples Matching!", cpuX + 40, tblY + 295);
          ctx.fillStyle = "#ffffff";
          ctx.font = "12px sans-serif";
          ctx.fillText("Matching Record IDs: R2, R5, R8", cpuX + 40, tblY + 325);
          ctx.fillStyle = "#a7f3d0";
          ctx.fillText("Zero disk blocks accessed to evaluate or count!", cpuX + 40, tblY + 350);

          // Benefits Callout
          ctx.fillStyle = "#cbd5e1";
          ctx.font = "12px sans-serif";
          ctx.fillText("• Physical I/O Optimization: Only the 3 matched records are", cpuX + 20, tblY + 415);
          ctx.fillText("  fetched from disk using direct row-offset calculation.", cpuX + 20, tblY + 435);
          ctx.fillStyle = "#facc15";
          ctx.fillText("• Massively popular in Data Warehousing & OLAP star schemas", cpuX + 20, tblY + 465);
          ctx.fillText("  for filtering dimensions with low distinct cardinalities.", cpuX + 20, tblY + 485);

          // Voice Spotlight Calibration
          if (t >= 0 && t < 15) {
            updateHUDTopic("Bitmap Concept");
          } else if (t >= 15 && t < 30) {
            drawSpotlightHighlight(ctx, tblX, tblY, tblW, tblH, "#38bdf8", "BIT VECTORS FOR LOW CARDINALITY", t);
            updateHUDTopic("Bit Vector Mapping");
          } else if (t >= 30 && t < 45) {
            drawSpotlightHighlight(ctx, cpuX, tblY, cpuW, tblH, "#10b981", "ALU BITWISE AND / OR / NOT", t);
            updateHUDTopic("Bitwise Logic Engine");
          } else {
            drawSpotlightHighlight(ctx, cpuX + 20, tblY + 265, cpuW - 40, 110, "#fde047", "POPCNT & ZERO I/O FILTERING", t);
            updateHUDTopic("POPCNT & Disk I/O");
          }
        }
      }
    ];

    // --- DOM Elements & Global Player State ---
    const canvas = document.getElementById('animCanvas');
    const ctx = canvas.getContext('2d');
    const playBtn = document.getElementById('playBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const timelineBar = document.getElementById('timelineBar');
    const timelineProgress = document.getElementById('timelineProgress');
    const currentTimeLabel = document.getElementById('currentTime');
    const totalDurationLabel = document.getElementById('totalDuration');
    const speedSelect = document.getElementById('speedSelect');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const muteBtn = document.getElementById('muteBtn');
    const muteIcon = document.getElementById('muteIcon');
    const ccToggleBtn = document.getElementById('ccToggleBtn');
    const onScreenCCContainer = document.getElementById('onScreenCCContainer');
    const subtitlesBox = document.getElementById('subtitlesBox');
    const externalSubtitles = document.getElementById('externalSubtitles');
    const closeOverlayCCBtn = document.getElementById('closeOverlayCCBtn');
    const sceneBadgeText = document.getElementById('sceneBadgeText');
    const currentSceneTitle = document.getElementById('currentSceneTitle');
    const currentSceneDuration = document.getElementById('currentSceneDuration');
    const currentSceneSummary = document.getElementById('currentSceneSummary');
    const sceneIconContainer = document.getElementById('sceneIconContainer');
    const playlistContainer = document.getElementById('playlistContainer');
    const formulaSheetContainer = document.getElementById('formulaSheetContainer');
    const tabScenesBtn = document.getElementById('tabScenesBtn');
    const tabFormulasBtn = document.getElementById('tabFormulasBtn');
    const hudCost = document.getElementById('hudCost');
    const hudTopic = document.getElementById('hudTopic');
    const voiceVisualizer = document.getElementById('voiceVisualizer');
    const liveFormulaMath = document.getElementById('liveFormulaMath');
    const liveFormulaCard = document.getElementById('liveFormulaCard');
    const toggleFormulaBtn = document.getElementById('toggleFormulaBtn');
    const toggleSandboxBtn = document.getElementById('toggleSandboxBtn');
    const sandboxModal = document.getElementById('sandboxModal');
    const closeSandboxBtn = document.getElementById('closeSandboxBtn');

    let currentSceneIdx = 0;
    let isPlaying = false;
    let isMuted = false;
    let playbackSpeed = 1.0;
    let isOverlayCCOpen = false;
    let isFormulaCardOpen = true;
    let activeSentenceIdx = -1;

    const audioPlayer = new Audio();
    audioPlayer.preload = 'auto';

    function formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    const totalDuration = AUDIO_DURATIONS.reduce((a, b) => a + b, 0);
    totalDurationLabel.textContent = formatTime(totalDuration);

    function resizeCanvas() {
      canvas.width = 1280;
      canvas.height = 720;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    function renderPlaylist() {
      playlistContainer.innerHTML = '';
      scenes.forEach((sc, idx) => {
        const item = document.createElement('div');
        item.className = `p-3 rounded-xl border cursor-pointer transition flex items-center justify-between gap-3 ${
          idx === currentSceneIdx 
            ? 'bg-cyan-950/80 border-cyan-500 shadow-lg shadow-cyan-500/20' 
            : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
        }`;
        item.onclick = () => selectScene(idx, true);

        item.innerHTML = `
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center text-sm">${sc.icon}</span>
            <div>
              <p class="font-semibold text-xs text-white leading-tight ${idx === currentSceneIdx ? 'text-cyan-300' : ''}">${sc.title}</p>
              <p class="text-[10px] text-slate-400 mt-0.5 playlist-sub">${Math.round(sc.duration)}s &bull; $${sc.hudCost}$</p>
            </div>
          </div>
          <span class="text-xs ${idx === currentSceneIdx ? 'text-cyan-400 font-bold' : 'text-slate-500'}">▶</span>
        `;
        playlistContainer.appendChild(item);
      });
    }

    // --- Dynamic Word-by-Word Karaoke Subtitles Engine ---
    function updateKaraokeSubtitles(t) {
      const sceneCues = SUBTITLES_DATA[currentSceneIdx] || [];
      if (!sceneCues || sceneCues.length === 0) return;

      let sIdx = 0;
      for (let i = 0; i < sceneCues.length; i++) {
        if (t >= sceneCues[i].start) {
          sIdx = i;
        }
      }

      const activeSentence = sceneCues[sIdx];
      if (!activeSentence) return;

      if (activeSentenceIdx !== sIdx) {
        activeSentenceIdx = sIdx;
        const wordsHtml = activeSentence.words.map((w, wIdx) => {
          return `<span id="word_${wIdx}" class="pending-word">${w.word}</span>`;
        }).join(' ');

        if (externalSubtitles) externalSubtitles.innerHTML = wordsHtml;
        if (subtitlesBox) subtitlesBox.innerHTML = wordsHtml;
      }

      const words = activeSentence.words;
      for (let wIdx = 0; wIdx < words.length; wIdx++) {
        const w = words[wIdx];
        const extSpan = externalSubtitles ? externalSubtitles.querySelector(`#word_${wIdx}`) : null;
        const ovSpan = subtitlesBox ? subtitlesBox.querySelector(`#word_${wIdx}`) : null;

        let cls = "pending-word";
        if (t >= w.start && t <= w.end) {
          cls = "active-word";
        } else if (t > w.end) {
          cls = "spoken-word";
        }

        if (extSpan && extSpan.className !== cls) extSpan.className = cls;
        if (ovSpan && ovSpan.className !== cls) ovSpan.className = cls;
      }
    }

    function selectScene(idx, autoPlay = false) {
      if (idx < 0) idx = 0;
      if (idx >= scenes.length) idx = scenes.length - 1;
      currentSceneIdx = idx;
      activeSentenceIdx = -1;

      const sc = scenes[currentSceneIdx];
      sceneBadgeText.textContent = `Scene ${sc.id + 1}: ${sc.title.split('.')[1] || sc.title}`;
      currentSceneTitle.textContent = sc.title;
      currentSceneDuration.textContent = `Duration: ${Math.round(sc.duration)}s`;
      currentSceneSummary.innerHTML = sc.summary;
      renderLatex(currentSceneSummary);
      updateLiveFormula(idx, 0);
      sceneIconContainer.textContent = sc.icon;
      if (window.katex) {
        try {
          katex.render(sc.hudCost, hudCost, { displayMode: false, throwOnError: false });
        } catch(e) { hudCost.textContent = sc.hudCost; }
      } else {
        hudCost.textContent = sc.hudCost;
      }

      updateKaraokeSubtitles(0);

      audioPlayer.src = sc.audioUri;
      audioPlayer.playbackRate = playbackSpeed;
      audioPlayer.currentTime = 0;

      renderPlaylist();

      if (autoPlay || isPlaying) {
        isPlaying = true;
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
        voiceVisualizer.classList.remove('opacity-0');
        voiceVisualizer.classList.add('opacity-100');
        audioPlayer.play().catch(e => console.log('Audio autoplay prevented:', e));
      } else {
        sc.render(ctx, 0, canvas.width, canvas.height);
      }
    }

    function renderLatex(element) {
      if (window.renderMathInElement) {
        try {
          renderMathInElement(element || document.body, {
            delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\\\(', right: '\\\\)', display: false},
              {left: '\\\\[', right: '\\\\]', display: true}
            ],
            throwOnError: false
          });
        } catch(e) { console.log('KaTeX auto-render error:', e); }
      }
    }

    // Comprehensive Scene-by-Scene LaTeX Formula Definitions
    const sceneFormulas = [
      // Scene 0: Disk Geometry
      [
        "\\\\text{Address} = (\\\\text{Surface } \\\\#, \\\\text{Track } \\\\#, \\\\text{Sector } \\\\#)",
        "T = s + \\\\frac{r}{2} + \\\\frac{b}{t} \\\\quad (s = \\\\text{Seek}, r/2 = \\\\text{Rotational Delay}, b/t = \\\\text{Transfer})",
        "\\\\text{Rotational Delay} = \\\\frac{60 \\\\times 1000}{2 \\\\times \\\\text{RPM}} \\\\text{ ms}",
        "\\\\text{Double Buffering: } \\\\max(\\\\text{CPU Processing}, \\\\text{Disk Transfer})"
      ],
      // Scene 1: Blocking Factor
      [
        "\\\\text{bfr} = \\\\left\\\\lfloor \\\\frac{B}{R} \\\\right\\\\rfloor \\\\quad (B = \\\\text{Block Size}, R = \\\\text{Record Size})",
        "b = \\\\left\\\\lceil \\\\frac{r}{\\\\text{bfr}} \\\\right\\\\rceil \\\\quad (r = \\\\text{Record Count})",
        "W = B - (\\\\text{bfr} \\\\times R) = B \\\\pmod R \\\\quad (\\\\text{Internal Fragmentation})",
        "\\\\text{Heap Scan: } \\\\frac{b}{2} \\\\quad \\\\text{vs Binary Search: } \\\\lceil \\\\log_2 b \\\\rceil"
      ],
      // Scene 2: Single-Level Indexes
      [
        "\\\\text{Primary Index: } b_I = \\\\left\\\\lceil \\\\frac{b}{\\\\text{bfr}_I} \\\\right\\\\rceil, \\\\quad \\\\text{Cost} = \\\\lceil \\\\log_2 b_I \\\\rceil + 1",
        "\\\\text{Clustering Index: } b_I = \\\\left\\\\lceil \\\\frac{d}{\\\\text{bfr}_I} \\\\right\\\\rceil, \\\\quad \\\\text{Cost} = \\\\lceil \\\\log_2 b_I \\\\rceil + \\\\left\\\\lceil \\\\frac{c}{\\\\text{bfr}} \\\\right\\\\rceil",
        "\\\\text{Secondary (Key): } b_I = \\\\left\\\\lceil \\\\frac{r}{\\\\text{bfr}_I} \\\\right\\\\rceil, \\\\quad \\\\text{Cost} = \\\\lceil \\\\log_2 b_I \\\\rceil + 1",
        "\\\\text{Secondary (Non-Key): Indirection Bucket Array eliminates duplicate index keys}"
      ],
      // Scene 3: Multi-Level & B+ Trees
      [
        "\\\\text{Fanout } fo = \\\\text{bfr}_I = \\\\left\\\\lfloor \\\\frac{B}{V + P} \\\\right\\\\rfloor",
        "\\\\text{Height } x = \\\\left\\\\lceil \\\\log_{fo}(b_{i1}) \\\\right\\\\rceil + 1",
        "\\\\text{B+ Tree Leaf: } p_{\\\\text{leaf}} \\\\times (P_{\\\\text{rec}} + V) + P_{\\\\text{next}} \\\\le B",
        "\\\\text{Point Cost: } x + 1 \\\\text{ I/Os} \\\\quad \\\\text{Range Cost: Direct leaf list traversal}"
      ],
      // Scene 4: Extendable Hashing
      [
        "\\\\text{Directory Size} = 2^d \\\\quad (d = \\\\text{Global Depth})",
        "\\\\text{Bucket Capacity } C, \\\\quad d' = \\\\text{Local Depth}",
        "d' = d \\\\implies d \\\\leftarrow d + 1 \\\\text{ (Directory Doubles!)}",
        "d' < d \\\\implies \\\\text{Bucket splits without directory expansion}"
      ],
      // Scene 5: Bitmap Indexing
      [
        "B_1 \\\\land B_2 \\\\quad (\\\\text{Bitwise AND for Intersection})",
        "B_1 \\\\lor B_2 \\\\quad (\\\\text{Bitwise OR for Union})",
        "\\\\neg B_1 \\\\quad (\\\\text{Bitwise NOT for Negation})",
        "\\\\text{Count} = \\\\text{POPCNT}(B_{\\\\text{result}}) \\\\quad (\\\\text{Zero Disk Reads})"
      ]
    ];

    function updateLiveFormula(sceneIdx, t) {
      if (!liveFormulaMath) return;
      const formulas = sceneFormulas[sceneIdx];
      if (!formulas || formulas.length === 0) return;
      const subIdx = Math.min(Math.floor((t / (AUDIO_DURATIONS[sceneIdx] || 60)) * formulas.length), formulas.length - 1);
      const curFormula = formulas[subIdx] || formulas[0];

      if (window.katex) {
        try {
          katex.render(curFormula, liveFormulaMath, { displayMode: false, throwOnError: false });
        } catch(e) { liveFormulaMath.textContent = curFormula; }
      } else {
        liveFormulaMath.textContent = curFormula;
      }
    }

    function updateHUDTopic(topic) {
      if (hudTopic) hudTopic.textContent = topic;
    }

    // Toggle Formula Banner
    if (toggleFormulaBtn) {
      toggleFormulaBtn.onclick = (e) => {
        e.stopPropagation();
        isFormulaCardOpen = !isFormulaCardOpen;
        if (isFormulaCardOpen) {
          liveFormulaCard.classList.remove('hidden');
        } else {
          liveFormulaCard.classList.add('hidden');
        }
      };
    }

    // On-Screen Subtitle Overlay Toggle & Draggable Logic
    if (ccToggleBtn && onScreenCCContainer) {
      ccToggleBtn.onclick = () => {
        isOverlayCCOpen = !isOverlayCCOpen;
        if (isOverlayCCOpen) {
          onScreenCCContainer.classList.remove('hidden');
          ccToggleBtn.classList.remove('text-slate-400');
          ccToggleBtn.classList.add('text-cyan-400', 'border-cyan-500');
        } else {
          onScreenCCContainer.classList.add('hidden');
          ccToggleBtn.classList.remove('text-cyan-400', 'border-cyan-500');
          ccToggleBtn.classList.add('text-slate-400');
        }
      };
    }

    if (closeOverlayCCBtn && onScreenCCContainer && ccToggleBtn) {
      closeOverlayCCBtn.onclick = () => {
        isOverlayCCOpen = false;
        onScreenCCContainer.classList.add('hidden');
        ccToggleBtn.classList.remove('text-cyan-400', 'border-cyan-500');
        ccToggleBtn.classList.add('text-slate-400');
      };
    }

    // Draggable On-Screen CC Logic
    let isDraggingCC = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let initialLeft = 0;
    let initialTop = 0;

    if (onScreenCCContainer) {
      const startDrag = (e) => {
        isDraggingCC = true;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        dragStartX = clientX;
        dragStartY = clientY;

        const rect = onScreenCCContainer.getBoundingClientRect();
        const parentRect = onScreenCCContainer.parentElement.getBoundingClientRect();
        initialLeft = rect.left - parentRect.left;
        initialTop = rect.top - parentRect.top;

        onScreenCCContainer.style.transform = 'none';
        onScreenCCContainer.style.left = `${initialLeft}px`;
        onScreenCCContainer.style.top = `${initialTop}px`;
        onScreenCCContainer.style.bottom = 'auto';
        document.body.style.userSelect = 'none';
      };

      const doDrag = (e) => {
        if (!isDraggingCC) return;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        const dx = clientX - dragStartX;
        const dy = clientY - dragStartY;
        onScreenCCContainer.style.left = `${initialLeft + dx}px`;
        onScreenCCContainer.style.top = `${initialTop + dy}px`;
      };

      const stopDrag = () => {
        isDraggingCC = false;
        document.body.style.userSelect = 'auto';
      };

      onScreenCCContainer.addEventListener('mousedown', startDrag);
      window.addEventListener('mousemove', doDrag);
      window.addEventListener('mouseup', stopDrag);

      onScreenCCContainer.addEventListener('touchstart', startDrag, { passive: true });
      window.addEventListener('touchmove', doDrag, { passive: true });
      window.addEventListener('touchend', stopDrag);
    }

    // --- Interactive Formula Sheet (Tab 2) ---
    function renderFormulaSheet() {
      if (!formulaSheetContainer) return;
      formulaSheetContainer.innerHTML = `
        <div class="space-y-4">
          <div class="p-3 rounded-xl border border-cyan-800/60 bg-cyan-950/40">
            <h4 class="font-bold text-cyan-300 text-xs mb-1">1. Physical Disk Latency</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$T = s + \\frac{r}{2} + \\frac{b}{t}$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Seek time $s$, rotational delay $r/2 = \\frac{60 \\times 1000}{2 \\times \\text{RPM}}$ ms, transfer time $b/t$.</p>
          </div>

          <div class="p-3 rounded-xl border border-blue-800/60 bg-blue-950/40">
            <h4 class="font-bold text-blue-300 text-xs mb-1">2. Blocking Factor & Block Count</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$\\text{bfr} = \\left\\lfloor \\frac{B}{R} \\right\\rfloor, \\quad b = \\left\\lceil \\frac{r}{\\text{bfr}} \\right\\rceil, \\quad W = B \\pmod R$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Unspanned wastes $W$ bytes per block. Spanned eliminates waste ($W=0$) via continuation pointers.</p>
          </div>

          <div class="p-3 rounded-xl border border-indigo-800/60 bg-indigo-950/40">
            <h4 class="font-bold text-indigo-300 text-xs mb-1">3. Single-Level Primary Index</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$r_I = b, \\quad \\text{bfr}_I = \\left\\lfloor \\frac{B}{V + P} \\right\\rfloor, \\quad b_I = \\left\\lceil \\frac{b}{\\text{bfr}_I} \\right\\rceil$$
              $$\\text{Search Cost} = \\lceil \\log_2 b_I \\rceil + 1 \\text{ Block Accesses}$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Sparse index on ordering key. 1 entry per data block.</p>
          </div>

          <div class="p-3 rounded-xl border border-purple-800/60 bg-purple-950/40">
            <h4 class="font-bold text-purple-300 text-xs mb-1">4. Multi-Level Index & B+ Tree Fanout</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$fo = \\text{bfr}_I, \\quad x = \\lceil \\log_{fo}(b_{i1}) \\rceil + 1$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Balanced B+ tree pushes all record pointers to leaves connected via doubly linked list.</p>
          </div>

          <div class="p-3 rounded-xl border border-emerald-800/60 bg-emerald-950/40">
            <h4 class="font-bold text-emerald-300 text-xs mb-1">5. Extendable Hashing Dynamics</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$\\text{Directory Size} = 2^d, \\quad d' = d \\implies d \\leftarrow d + 1$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Directory doubles only if local depth equals global depth upon bucket overflow.</p>
          </div>

          <div class="p-3 rounded-xl border border-amber-800/60 bg-amber-950/40">
            <h4 class="font-bold text-amber-300 text-xs mb-1">6. Bitmap Multi-Attribute Filtering</h4>
            <div class="math-block overflow-x-auto text-yellow-300 py-1">
              $$B_{\\text{res}} = B_1 \\land B_2 \\land \\dots \\land B_k, \\quad \\text{Count} = \\text{POPCNT}(B_{\\text{res}})$$
            </div>
            <p class="text-[10px] text-slate-400 mt-1">Evaluated entirely in CPU registers with zero disk block reads.</p>
          </div>
        </div>
      `;
      renderLatex(formulaSheetContainer);
    }

    if (tabScenesBtn && tabFormulasBtn) {
      tabScenesBtn.onclick = () => {
        tabScenesBtn.classList.remove('text-slate-400');
        tabScenesBtn.classList.add('bg-cyan-600', 'text-white');
        tabFormulasBtn.classList.remove('bg-cyan-600', 'text-white');
        tabFormulasBtn.classList.add('text-slate-400');
        playlistContainer.classList.remove('hidden');
        formulaSheetContainer.classList.add('hidden');
      };
      tabFormulasBtn.onclick = () => {
        tabFormulasBtn.classList.remove('text-slate-400');
        tabFormulasBtn.classList.add('bg-cyan-600', 'text-white');
        tabScenesBtn.classList.remove('bg-cyan-600', 'text-white');
        tabScenesBtn.classList.add('text-slate-400');
        playlistContainer.classList.add('hidden');
        formulaSheetContainer.classList.remove('hidden');
        renderFormulaSheet();
      };
    }

    // --- Interactive Sandbox Logic ---
    function updateSandboxCalculations() {
      // 1. Disk Latency
      const rpm = parseFloat(document.getElementById('inputRpm').value) || 7200;
      const seek = parseFloat(document.getElementById('inputSeek').value) || 8.0;
      const transferRate = parseFloat(document.getElementById('inputTransfer').value) || 100;

      document.getElementById('valRpm').textContent = rpm;
      document.getElementById('valSeek').textContent = seek.toFixed(1) + " ms";
      document.getElementById('valTransfer').textContent = transferRate + " MB/s";

      const rotDelay = (60 * 1000) / (2 * rpm);
      const transTime = (4 / (transferRate * 1024)) * 1000;
      const totalLat = seek + rotDelay + transTime;
      const iops = Math.round(1000 / totalLat);

      document.getElementById('resRotDelay').textContent = rotDelay.toFixed(2) + " ms";
      document.getElementById('resTransTime').textContent = transTime.toFixed(3) + " ms";
      document.getElementById('resTotalLatency').textContent = totalLat.toFixed(2) + " ms";
      document.getElementById('resIops').textContent = iops + " IOPS";

      const formulaDiv = document.getElementById('sandboxLatencyFormula');
      if (formulaDiv && window.katex) {
        const tex = `T = ${seek.toFixed(1)} + ${rotDelay.toFixed(2)} + ${transTime.toFixed(3)} = \\mathbf{${totalLat.toFixed(2)}\\text{ ms}} \\implies ${iops}\\text{ IOPS}`;
        try {
          katex.render(tex, formulaDiv, { displayMode: true, throwOnError: false });
        } catch(e) {}
      }

      // 2. Blocking Factor & Index Levels
      const r = parseInt(document.getElementById('inputRecs').value) || 100000;
      const R = parseInt(document.getElementById('inputRecSize').value) || 200;
      const B = parseInt(document.getElementById('inputBlockSize').value) || 4096;
      const entrySize = parseInt(document.getElementById('inputIndexEntry').value) || 16;

      const bfr = Math.floor(B / R);
      const b = Math.ceil(r / bfr);
      const fo = Math.floor(B / entrySize);
      const bI = Math.ceil(b / fo);
      const height = Math.ceil(Math.log(b) / Math.log(fo));

      document.getElementById('resBfr').textContent = bfr + " recs/blk";
      document.getElementById('resDataBlocks').textContent = b.toLocaleString();
      document.getElementById('resFanout').textContent = fo.toLocaleString();
      document.getElementById('resIndexBlocks').textContent = bI.toLocaleString();
      document.getElementById('resTreeHeight').textContent = height + " levels";

      // Showdown costs
      const heapCost = Math.round(b / 2);
      const binCost = Math.ceil(Math.log2(b));
      const primCost = Math.ceil(Math.log2(bI)) + 1;
      const btreeCost = height + 1;

      document.getElementById('resHeapCost').textContent = heapCost.toLocaleString() + " I/Os";
      document.getElementById('resBinCost').textContent = binCost + " I/Os";
      document.getElementById('resPrimCost').textContent = primCost + " I/Os";
      document.getElementById('resBTreeCost').textContent = btreeCost + " I/Os";
    }

    if (toggleSandboxBtn && sandboxModal) {
      toggleSandboxBtn.onclick = () => {
        sandboxModal.classList.remove('hidden');
        updateSandboxCalculations();
      };
    }
    if (closeSandboxBtn && sandboxModal) {
      closeSandboxBtn.onclick = () => sandboxModal.classList.add('hidden');
    }

    ['inputRpm', 'inputSeek', 'inputTransfer', 'inputRecs', 'inputRecSize', 'inputBlockSize', 'inputIndexEntry'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('input', updateSandboxCalculations);
    });

    // --- In-Browser Video Recording & Export Engine (MediaRecorder API) ---
    let mediaRecorder = null;
    let recordedChunks = [];
    let isRecordingActive = false;
    let recordMode = 'single';

    const exportVideoBtn = document.getElementById('exportVideoBtn');
    const exportModal = document.getElementById('exportModal');
    const closeExportModalBtn = document.getElementById('closeExportModalBtn');
    const btnExportScene = document.getElementById('btnExportScene');
    const btnExportFull = document.getElementById('btnExportFull');
    const recordingBanner = document.getElementById('recordingBanner');
    const recordingText = document.getElementById('recordingText');
    const cancelRecordBtn = document.getElementById('cancelRecordBtn');

    if (exportVideoBtn && exportModal) {
      exportVideoBtn.onclick = () => exportModal.classList.remove('hidden');
    }
    if (closeExportModalBtn && exportModal) {
      closeExportModalBtn.onclick = () => exportModal.classList.add('hidden');
    }

    let audioCaptureCtx = null;
    let audioCaptureSource = null;
    let audioCaptureDest = null;

    function setupAudioStream() {
      if (!audioCaptureCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
          try {
            audioCaptureCtx = new AudioContextClass();
            audioCaptureSource = audioCaptureCtx.createMediaElementSource(audioPlayer);
            audioCaptureDest = audioCaptureCtx.createMediaStreamDestination();
            audioCaptureSource.connect(audioCaptureDest);
            audioCaptureSource.connect(audioCaptureCtx.destination);
          } catch(e) {
            console.log('Audio capture setup warning:', e);
          }
        }
      }
    }

    function startRecordingWorkflow(mode) {
      exportModal.classList.add('hidden');
      setupAudioStream();
      recordedChunks = [];
      recordMode = mode;
      isRecordingActive = true;

      const canvasStream = canvas.captureStream(30);
      const tracks = [...canvasStream.getVideoTracks()];
      if (audioCaptureDest && audioCaptureDest.stream) {
        tracks.push(...audioCaptureDest.stream.getAudioTracks());
      }

      const combinedStream = new MediaStream(tracks);

      let chosenMime = 'video/mp4';
      const mimes = ['video/mp4;codecs=avc1,mp4a.40.2', 'video/mp4', 'video/webm;codecs=vp9,opus', 'video/webm'];
      for (const m of mimes) {
        if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) {
          chosenMime = m;
          break;
        }
      }

      try {
        mediaRecorder = new MediaRecorder(combinedStream, {
          mimeType: chosenMime,
          videoBitsPerSecond: 4000000
        });
      } catch(e) {
        mediaRecorder = new MediaRecorder(combinedStream);
      }

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) recordedChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        isRecordingActive = false;
        recordingBanner.classList.add('hidden');
        const ext = chosenMime.includes('mp4') ? 'mp4' : 'webm';
        const blob = new Blob(recordedChunks, { type: chosenMime });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const name = recordMode === 'full' 
          ? 'Chapter1_Physical_Storage_Complete_Masterclass' 
          : `Chapter1_Scene_${currentSceneIdx + 1}_${scenes[currentSceneIdx].title.replace(/[^a-zA-Z0-9]/g, '_')}`;
        a.download = `${name}.${ext}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 10000);
      };

      recordingBanner.classList.remove('hidden');
      recordingText.textContent = mode === 'full'
        ? 'RECORDING FULL MASTERCLASS (AUTO-SAVES AT END)...'
        : `RECORDING SCENE ${currentSceneIdx + 1} (AUTO-SAVES AT END)...`;

      mediaRecorder.start(1000);

      if (mode === 'full') {
        selectScene(0, true);
      } else {
        audioPlayer.currentTime = 0;
        if (!isPlaying) togglePlay();
      }
    }

    if (btnExportScene) {
      btnExportScene.onclick = () => startRecordingWorkflow('single');
    }
    if (btnExportFull) {
      btnExportFull.onclick = () => startRecordingWorkflow('full');
    }
    if (cancelRecordBtn) {
      cancelRecordBtn.onclick = () => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
        }
      };
    }

    function togglePlay() {
      if (isPlaying) {
        isPlaying = false;
        audioPlayer.pause();
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
        voiceVisualizer.classList.add('opacity-0');
        voiceVisualizer.classList.remove('opacity-100');
      } else {
        isPlaying = true;
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
        voiceVisualizer.classList.remove('opacity-0');
        voiceVisualizer.classList.add('opacity-100');
        if (!audioPlayer.src || audioPlayer.src === '') {
          audioPlayer.src = scenes[currentSceneIdx].audioUri;
        }
        audioPlayer.playbackRate = playbackSpeed;
        audioPlayer.play().catch(e => console.log('Playback error:', e));
      }
    }

    playBtn.onclick = togglePlay;
    prevBtn.onclick = () => selectScene(currentSceneIdx - 1, isPlaying);
    nextBtn.onclick = () => selectScene(currentSceneIdx + 1, isPlaying);

    audioPlayer.ontimeupdate = () => {
      const sceneTime = audioPlayer.currentTime;
      let elapsed = 0;
      for (let i = 0; i < currentSceneIdx; i++) elapsed += scenes[i].duration;
      elapsed += sceneTime;

      currentTimeLabel.textContent = formatTime(elapsed);
      timelineProgress.style.width = `${(elapsed / totalDuration) * 100}%`;

      updateKaraokeSubtitles(sceneTime);
      updateLiveFormula(currentSceneIdx, sceneTime);
    };

    audioPlayer.onended = () => {
      if (isRecordingActive) {
        if (recordMode === 'single' || currentSceneIdx === scenes.length - 1) {
          if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
        }
      }

      if (currentSceneIdx < scenes.length - 1) {
        selectScene(currentSceneIdx + 1, true);
      } else {
        isPlaying = false;
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
        voiceVisualizer.classList.add('opacity-0');
      }
    };

    timelineBar.onclick = (e) => {
      const rect = timelineBar.getBoundingClientRect();
      const ratio = (e.clientX - rect.left) / rect.width;
      const targetTime = ratio * totalDuration;

      let acc = 0;
      for (let i = 0; i < scenes.length; i++) {
        if (acc + scenes[i].duration >= targetTime) {
          const offset = targetTime - acc;
          selectScene(i, isPlaying);
          audioPlayer.currentTime = offset;
          updateKaraokeSubtitles(offset);
          return;
        }
        acc += scenes[i].duration;
      }
    };

    speedSelect.onchange = () => {
      playbackSpeed = parseFloat(speedSelect.value);
      audioPlayer.playbackRate = playbackSpeed;
    };

    muteBtn.onclick = () => {
      isMuted = !isMuted;
      audioPlayer.muted = isMuted;
      muteIcon.textContent = isMuted ? '🔇' : '🔊';
    };

    fullscreenBtn.onclick = () => {
      const cont = document.getElementById('videoContainer');
      if (!document.fullscreenElement) {
        cont.requestFullscreen().catch(e => console.log(e));
      } else {
        document.exitFullscreen().catch(e => console.log(e));
      }
    };

    function drawRecordingOverlay(ctx, t, w, h) {
      ctx.save();
      const scIdx = currentSceneIdx;
      const sc = scenes[scIdx];

      const formulas = [
        "T = s + r/2 + b/t | Address = (Surface, Track, Sector)",
        "bfr = ⌊B/R⌋ | b = ⌈r/bfr⌉ | Waste = B mod R",
        "Primary: ⌈log₂(b_I)⌉ + 1 | Cluster: ⌈log₂(b_I)⌉ + ⌈c/bfr⌉",
        "B+ Tree: fo = bfr_I | Height x = ⌈log_fo(b_i1)⌉ + 1",
        "Directory = 2^d | Split: d' = d ⇒ d ← d + 1",
        "Bitwise: B₁ ∧ B₂ | POPCNT = Instant Count"
      ];
      const formulaText = formulas[scIdx] || sc.hudCost || "";
      if (formulaText) {
        ctx.font = "bold 13px Inter, monospace, sans-serif";
        const fWidth = ctx.measureText(formulaText).width + 30;
        const chipX = w - fWidth - 30;
        const chipY = 22;
        const chipH = 34;

        ctx.fillStyle = "rgba(15, 23, 42, 0.90)";
        ctx.strokeStyle = "rgba(6, 182, 212, 0.5)";
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.roundRect(chipX, chipY, fWidth, chipH, 8);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "#38bdf8";
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

        ctx.fillStyle = "rgba(10, 15, 29, 0.94)";
        ctx.strokeStyle = "rgba(6, 182, 212, 0.45)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(pillX, pillY, pillW, pillH, 10);
        ctx.fill();
        ctx.stroke();

        const firstLineY = lines.length === 1 ? (pillY + pillH / 2) : (pillY + 22);

        lines.forEach((ln, lIdx) => {
          const lineY = firstLineY + lIdx * lineH;
          let startWordX = (w - ln.totalW) / 2;
          ctx.textAlign = "left";

          for (let wm of ln.words) {
            const wordText = wm.word + " ";
            const wordW = ctx.measureText(wordText).width;
            if (t >= wm.start && t <= wm.end) {
              ctx.fillStyle = "#38bdf8";
              ctx.shadowColor = "#0284c7";
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
    }

    // --- 60fps Dynamic Animation Rendering Loop ---
    function animLoop() {
      const curT = audioPlayer.currentTime || 0;
      const sc = scenes[currentSceneIdx];
      if (sc && sc.render) {
        sc.render(ctx, curT, canvas.width, canvas.height);
      }
      if (isRecordingActive) {
        drawRecordingOverlay(ctx, curT, canvas.width, canvas.height);
      }
      requestAnimationFrame(animLoop);
    }
    requestAnimationFrame(animLoop);


    // Initial Scene Setup
    selectScene(0, false);
    renderFormulaSheet();
    updateSandboxCalculations();
  </script>
</body>
</html>
"""

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Successfully generated chapter1.html ({os.path.getsize(output_html_path)} bytes)")
