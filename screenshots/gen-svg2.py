#!/usr/bin/env python3
"""
Generate a standalone animated SVG terminal recording from an asciicast v2 file.
Fixed version with proper CSS animation keyframes.
"""
import json
import html
import math

def generate_terminal_svg(cast_file, output_file, width=800, height=500):
    with open(cast_file) as f:
        header = json.loads(f.readline())
        frames_raw = [json.loads(line) for line in f.readlines()]
    
    screen_width = header['width']
    screen_height = header['height']
    
    # Reconstruct screen state with snapshots
    snapshots = []
    screen = [[" "] * screen_width for _ in range(screen_height)]
    cursor_x = 0
    cursor_y = 0
    
    SNAPSHOT_INTERVAL = 0.2  # seconds
    
    def take_snapshot(t):
        lines = [''.join(row) for row in screen]
        snapshots.append((t, lines[:]))
    
    ts = 0
    last_snap_time = 0
    
    for ts, event_type, data in frames_raw:
        if event_type != 'o':
            continue
        
        i = 0
        while i < len(data):
            ch = data[i]
            if ch == '\033':  # ANSI escape
                i += 1
                while i < len(data) and data[i] not in 'mHABCDsf':
                    if data[i] == '?':
                        i += 1
                        while i < len(data) and data[i] not in 'hl':
                            i += 1
                    i += 1
                i += 1
                continue
            elif ch == '\r':
                cursor_x = 0
                i += 1
                continue
            elif ch == '\n':
                cursor_x = 0
                cursor_y += 1
                if cursor_y >= screen_height:
                    screen.pop(0)
                    screen.append([" "] * screen_width)
                    cursor_y = screen_height - 1
                i += 1
                continue
            elif ord(ch) < 32:
                i += 1
                continue
            else:
                if cursor_x < screen_width and cursor_y < screen_height:
                    screen[cursor_y][cursor_x] = ch
                cursor_x += 1
                if cursor_x >= screen_width:
                    cursor_x = 0
                    cursor_y += 1
                    if cursor_y >= screen_height:
                        screen.pop(0)
                        screen.append([" "] * screen_width)
                        cursor_y = screen_height - 1
                i += 1
        
        if ts - last_snap_time >= SNAPSHOT_INTERVAL:
            take_snapshot(ts)
            last_snap_time = ts
    
    # Final snapshot
    take_snapshot(ts + 0.1)
    
    duration = snapshots[-1][0] + 0.5
    n = len(snapshots)
    
    print(f"Duration: {duration:.1f}s, Frames: {n}")
    
    # SVG dimensions
    font_family = "Menlo, Monaco, 'Courier New', monospace"
    font_size = 14
    char_w = font_size * 0.62
    char_h = font_size * 1.4
    pad = 20
    
    svg_w = int(char_w * screen_width + pad * 2)
    svg_h = int(char_h * screen_height + pad * 2 + 40)
    title_bar_h = 35
    
    # Colors
    bg = "#1a1b26"
    title_bg = "#24283b"
    text_color = "#a9b1d6"
    prompt_color = "#7aa2f7"
    heading_color = "#9ece6a"
    dim_color = "#565f89"
    accent = "#bb9af7"
    cursor_color = "#c0caf5"
    
    def esc(s):
        return html.escape(s)
    
    # CSS keyframes approach: use @keyframes with step-based animation
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">')
    lines.append(f'<defs>')
    lines.append(f'<style>')
    lines.append(f'@keyframes cursor-bl {{{"from,to{opacity:1}50%{opacity:0}"}}}')
    
    # Generate a single @keyframes for the entire terminal content
    # Each frame is a CSS keyframe step
    lines.append(f'.terminal {{ font-family: {esc(font_family)}; font-size: {font_size}px; }}')
    lines.append(f'</style>')
    lines.append(f'</defs>')
    
    # Background
    lines.append(f'<rect width="100%" height="100%" rx="8" fill="{bg}" />')
    
    # Title bar
    lines.append(f'<rect x="0" y="0" width="100%" height="{title_bar_h}" rx="8" fill="{title_bg}" />')
    lines.append(f'<rect x="0" y="{title_bar_h-10}" width="100%" height="10" fill="{title_bg}" />')
    
    # Dots
    for dx, col in [(14, "#ff5f57"), (30, "#fdbc40"), (46, "#33c748")]:
        lines.append(f'<circle cx="{dx}" cy="17" r="5" fill="{col}" opacity="0.8" />')
    
    title = f"hermes-core-skills — Quick Install Demo ({screen_width}x{screen_height})"
    lines.append(f'<text x="{svg_w//2}" y="24" text-anchor="middle" fill="{dim_color}" font-family="{esc(font_family)}" font-size="12">{esc(title)}</text>')
    
    # For each snapshot, create a group with opacity animation
    for idx, (t, scr_lines) in enumerate(snapshots):
        start = (t / duration) * 100
        if idx < n - 1:
            end = (snapshots[idx+1][0] / duration) * 100
        else:
            end = 100.0
        
        gid = f"f{idx}"
        lines.append(f'<g id="{gid}">')
        
        # Show current frame, hide all others using CSS animation
        # Each frame fades in at its start time and fades out at next frame's start
        lines.append(f'<animate attributeName="opacity" dur="{duration}s" repeatCount="indefinite" '
                     f'keyTimes="0;{max(0,start-0.1)/100:.4f};{start/100:.4f};{end/100:.4f};{min(100,end+0.1)/100:.4f};1" '
                     f'values="0;0;1;1;0;0" />')
        
        y = title_bar_h + pad
        for li, ln in enumerate(scr_lines[:screen_height]):
            if not ln.strip() and idx >= n-2 and li > screen_height - 3:
                continue
            escaped = esc(ln.rstrip())
            
            # Color-code some lines for visual variety
            if 'Step' in ln or '✓' in ln:
                fill = heading_color
            elif '$ ' in ln:
                fill = prompt_color
            elif '#' in ln and not ln.strip().startswith('#'):
                fill = dim_color
            elif '─' in ln or '╔' in ln or '║' in ln or '╚' in ln:
                fill = accent
            else:
                fill = text_color
            
            lines.append(f'<text class="terminal" x="{pad}" y="{y}" fill="{fill}">{escaped}</text>')
            y += char_h
        
        lines.append('</g>')
    
    # Final blinking cursor
    final_y = title_bar_h + pad + 16 * char_h
    final_x = pad + int(40 * char_w)
    lines.append(f'<rect x="{final_x}" y="{final_y - font_size + 4}" width="{char_w}" height="{font_size}" fill="{cursor_color}" opacity="0.6">')
    lines.append(f'  <animate attributeName="opacity" values="0.6;0;0.6" dur="1.2s" repeatCount="indefinite" />')
    lines.append('</rect>')
    
    lines.append('</svg>')
    
    svg_content = '\n'.join(lines)
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"Generated: {output_file} ({svg_w}x{svg_h}, {n} frames)")
    return output_file

if __name__ == "__main__":
    generate_terminal_svg("demo.cast", "demo.svg")
