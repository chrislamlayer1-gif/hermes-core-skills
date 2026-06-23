#!/usr/bin/env python3
"""
Generate a standalone animated SVG terminal recording from an asciicast v2 file.
No external dependencies — pure Python SVG generation.
"""
import json
import html
import textwrap

def generate_terminal_svg(cast_file, output_file, width=800, height=500):
    with open(cast_file) as f:
        header = json.loads(f.readline())
        frames_raw = [json.loads(line) for line in f.readlines()]
    
    # Reconstruct the screen state over time
    screen_width = header['width']
    screen_height = header['height']
    
    # Snapshots: list of (time, screen_lines)
    snapshots = []
    screen = [[" "] * screen_width for _ in range(screen_height)]
    # Track cursor position
    cursor_x = 0
    cursor_y = 0
    ansi_buffer = ""
    
    last_time = 0
    snapshot_interval = 0.15  # seconds between snapshots for GIF-like pacing
    
    def flush_screen(t):
        nonlocal last_time
        if t - last_time >= snapshot_interval:
            lines = [''.join(row) for row in screen]
            snapshots.append((t, lines[:]))
            last_time = t
    
    for ts, event_type, data in frames_raw:
        if event_type == 'o':
            # Process output data - strip ANSI for SVG text rendering
            # Keep only printable characters
            chars = []
            i = 0
            while i < len(data):
                ch = data[i]
                if ch == '\033':  # ANSI escape
                    # Skip until 'm' (for now, keep it simple)
                    i += 1
                    while i < len(data) and data[i] not in 'mHABCD':
                        if data[i] == '?':
                            i += 1
                            while i < len(data) and data[i] not in 'hl':
                                i += 1
                            i += 1
                            continue
                        i += 1
                    if i < len(data):
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
                        # Scroll
                        screen.pop(0)
                        screen.append([" "] * screen_width)
                        cursor_y = screen_height - 1
                    i += 1
                    continue
                elif ord(ch) < 32:  # Other control chars
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
            
            flush_screen(ts)
    
    # Also add final state
    snapshots.append((ts, [''.join(row) for row in screen]))
    
    # Now generate SVG with CSS animation
    duration = snapshots[-1][0] + 1.0  # total duration in seconds
    frame_duration = duration / max(len(snapshots), 1)
    
    # Font settings
    font_family = "Menlo, Monaco, 'Courier New', monospace"
    font_size = 14
    char_w = font_size * 0.62
    char_h = font_size * 1.35
    padding = 20
    
    svg_w = int(char_w * screen_width + padding * 2)
    svg_h = int(char_h * screen_height + padding * 2 + 35)  # +35 for title bar
    
    # Colors (dark terminal theme)
    bg = "#1a1b26"
    title_bg = "#2f3340"
    text_color = "#c0caf5"
    prompt_color = "#7aa2f7"
    success_color = "#9ece6a"
    accent_color = "#bb9af7"
    dim_color = "#565f89"
    
    # Title bar
    title = f"hermes-core-skills — Quick Install Demo ({screen_width}x{screen_height})"
    
    def escape_svg(s):
        return html.escape(s)
    
    lines_out = []
    lines_out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">')
    lines_out.append(f'<defs><style>@keyframes type{{from{{opacity:0}}to{{opacity:1}}}}</style></defs>')
    
    # Background
    lines_out.append(f'<rect width="{svg_w}" height="{svg_h}" rx="8" fill="{bg}" />')
    
    # Title bar
    lines_out.append(f'<rect x="0" y="0" width="{svg_w}" height="35" rx="8" fill="{title_bg}" />')
    lines_out.append(f'<rect x="0" y="25" width="{svg_w}" height="10" fill="{title_bg}" />')
    
    # Traffic light dots
    for i, (cx, fill) in enumerate([(14, "#ff5f57"), (30, "#fdbc40"), (46, "#33c748")]):
        lines_out.append(f'<circle cx="{cx}" cy="17" r="5" fill="{fill}" opacity="0.8" />')
    
    lines_out.append(f'<text x="{svg_w//2}" y="24" text-anchor="middle" fill="{dim_color}" font-family="{font_family}" font-size="12">{escape_svg(title)}</text>')
    
    # Terminal content
    for frame_idx, (ts, lines) in enumerate(snapshots):
        # Frame visibility: shown only during its time window
        start_pct = (frame_idx * frame_duration / duration) * 100
        end_pct = ((frame_idx + 1) * frame_duration / duration) * 100
        
        # For all frames except last, show until next frame
        if frame_idx < len(snapshots) - 1:
            display_range = f"{start_pct}%"
        else:
            display_range = f"{start_pct}%"
        
        # Actually, show current frame and hide all previous frames
        # Using CSS animation: each frame is shown for a portion
        group_id = f"f{frame_idx}"
        
        lines_out.append(f'<g id="{group_id}" opacity="0">')
        lines_out.append(f'  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{start_pct/100-0.001:.4f};{start_pct/100:.4f};{end_pct/100:.4f};{end_pct/100+0.001:.4f};1" dur="{duration}s" repeatCount="indefinite" />')
        
        y = 48
        for line_idx, line in enumerate(lines):
            if line_idx >= screen_height:
                break
            escaped = escape_svg(line.rstrip())
            if line_idx == 16:  # where Step 4 text appears
                lines_out.append(f'  <text x="{padding}" y="{y}" fill="{success_color}" font-family="{font_family}" font-size="{font_size}">{escaped}</text>')
            else:
                lines_out.append(f'  <text x="{padding}" y="{y}" fill="{text_color}" font-family="{font_family}" font-size="{font_size}">{escaped}</text>')
            y += char_h
        
        lines_out.append('</g>')
    
    # Steady-state final frame (shows when animation loops are done, or as snapshot)
    # Add subtle cursor blink
    lines_out.append(f'<rect x="{padding}" y="{padding + 16*char_h}" width="{char_w}" height="{font_size+2}" fill="{accent_color}" opacity="0.5">')
    lines_out.append('  <animate attributeName="opacity" values="0.5;0;0.5" dur="1s" repeatCount="indefinite" />')
    lines_out.append('</rect>')
    
    lines_out.append('</svg>')
    
    svg_content = '\n'.join(lines_out)
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"Generated SVG: {output_file}")
    print(f"  Dimensions: {svg_w}x{svg_h}")
    print(f"  Frames: {len(snapshots)}")
    print(f"  Duration: {duration:.1f}s")
    return output_file

if __name__ == "__main__":
    generate_terminal_svg("demo.cast", "demo.svg")
