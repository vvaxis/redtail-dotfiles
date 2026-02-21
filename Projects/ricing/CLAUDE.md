# Redtail — Ricing Project

This is the ricing workspace for **redtail**, the Arch Linux + Niri desktop environment on João Vítor's secondary machine. The actual dotfiles live in `$HOME` managed by yadm; this project (`~/Projects/ricing`) holds conversation context, reference material, and guides.

---

## The Machine

- **Hostname:** redtail
- **Hardware:** Lenovo IdeaPad 3 15ALC6
- **CPU:** AMD Ryzen 5 5500U (6C/12T, up to 4.0 GHz)
- **GPU:** AMD Radeon Lucienne (integrated)
- **RAM:** 6 GB DDR4 (soldered, not upgradeable to 8) — zram 8 GB (zstd)
- **Storage:** 256 GB NVMe (SSSTC CL1-4D256)
- **Display:** 15.6" 1920x1080
- **WiFi/BT:** RTL8822CU (wpa_supplicant backend)
- **Kernel:** linux-lts 6.12.x (linux mainline also installed as fallback)
- **Firmware quirk:** Fn lock is inverted relative to the F-row — media keys are direct, F-keys require Fn. Not fixable without losing media key access. Print Screen requires Fn+PrtSc.

This is a daily-carry college notebook. It reads PDFs and articles, writes text (Google Docs, .txt, occasionally .docx), codes occasionally, and sometimes runs games. RAM is tight at 6 GB — keep this in mind when suggesting daemons or heavy processes.

**Display density note:** 15.6" at 1080p is dense — UI text is physically small. Font sizes across configs should be **14px minimum**, ideally larger where aesthetically appropriate. Don't default to 11-12px for any user-facing text.

## The User

João Vítor de Carvalho Almeida, 21, São Paulo. FGV EAESP undergraduate in Public Administration. President of the Conselho Municipal dos Direitos da Juventude de São Paulo. See `PROFILE.md` for full details.

**Communication style:** Direct, corrects frequently, expects no hand-holding. Speaks Brazilian Portuguese natively, English fluently. Will say "é cinza, não marrom" if the brown you picked reads gray on his screen. Trust his perception over theory.

**Relevant preferences:**
- Prefers practical, actionable changes over abstract improvements
- Has an epic-humanist sensibility with a melancholic inclination — this influences the aesthetic direction
- Games taste includes Disco Elysium, Suzerain, Sir Brante — narrative depth, moral weight, strong aesthetics as language
- Vasco da Gama supporter (the ASCII Vasco logo in one of his reference rices is not a coincidence)

## The Stack

### Core

| Layer | Component |
|---|---|
| OS | Arch Linux |
| Compositor | Niri (scrollable tiling Wayland) |
| Shell | zsh (grml-zsh-config base) |
| Prompt | Starship |
| Terminal | Foot |
| Launcher | Fuzzel |
| Notifications | Dunst |
| Lock screen | swaylock-effects |
| Wallpaper | swaybg (static) |
| File manager | Nemo (GUI), Yazi (TUI) |
| Editor | Micro (TUI), occasionally code in other editors |
| Browser | Zen Browser |
| System monitor | btop |
| PDF viewer | Zathura |
| Image viewer | imv |
| Video player | mpv |
| Audio | PipeWire + WirePlumber |
| Bluetooth | BlueZ + Blueman |
| Network | NetworkManager + networkmanager-dmenu |
| Volume control | pwvucontrol |
| Clipboard | cliphist + wl-clipboard |
| Screenshots | grim + slurp |
| Brightness | brightnessctl |
| Idle/power | swayidle, power-profiles-daemon |
| Greeter | greetd + tuigreet |
| Dotfile management | yadm |
| AUR helper | yay |
| Music | spotify-player (Rust TUI, Spotify Connect, MPRIS) |
| Bar | Ignis (vertical sidebar, replaces Waybar) |
| Dashboard | Ignis (overlay — toggled via Mod+D) |

### Fonts

- **Monospace (everywhere):** Iosevka Nerd Font (`ttf-iosevka-nerd`)
- **Unicode/CJK fallback:** Noto Fonts CJK (`noto-fonts-cjk`)
- **Emoji:** Noto Color Emoji (`noto-fonts-emoji`)

### Cursor & Icons

- **Cursor:** phinger-cursors-dark, size 24 (set in `.zprofile` and niri gsettings)
- **Icons:** Papirus-Dark
- **GTK theme:** adw-gtk-theme (Adwaita dark, overridden by GTK CSS)

### Security

- **Firewall:** ufw (deny incoming, allow outgoing)
- **DNS:** DNS-over-TLS via systemd-resolved, primary Quad9 (`9.9.9.9`, `149.112.112.112`), fallback Cloudflare + Google

### AUR Packages

bibata-cursor-theme-bin, networkmanager-dmenu-git, phinger-cursors, pwvucontrol, swaylock-effects, yay, zen-browser-bin

### System Services (enabled)

**System-level:** bluetooth, greetd, NetworkManager, systemd-resolved, ufw

**User-level:** wireplumber, pipewire, pipewire-pulse, battery-notify.timer

### Not Yet Installed (anticipated)

The system was recently formatted. Many packages the user will eventually need are not yet installed. Examples from past discussion: `bat` (aliased but not present — falls back to cat). Don't assume a package is available just because it's common; check first.

## Config Organization

All configuration lives under `~/.config/` with standard XDG paths. Key directories:

```
~/.config/
├── autostart/          # nm-applet.desktop (Hidden=true — disabled)
├── btop/
│   ├── btop.conf
│   └── themes/redtail.theme
├── dashboard/          # Google Calendar credentials + token
├── dunst/dunstrc
├── foot/foot.ini
├── fuzzel/fuzzel.ini
├── gtk-3.0/gtk.css     # palette CSS variables (legacy + libadwaita) + widget overrides
├── gtk-4.0/
│   ├── gtk.css         # palette CSS variables
│   └── settings.ini    # gtk-hint-font-metrics=true
├── ignis/
│   ├── config.py       # sidebar + dashboard window definitions
│   ├── style.css       # shared CSS for sidebar + dashboard
│   ├── modules/        # sidebar modules (power, clock, volume, etc.)
│   ├── modules/dashboard/  # dashboard cards (calendar, events, weather, notes, music)
│   └── scripts/        # weather.py, gcal-events.py, .venv/, requirements.txt
├── micro/
│   ├── colorschemes/redtail.micro
│   └── settings.json
├── niri/config.kdl
├── spotify-player/
│   ├── app.toml        # layout, playback, cover art, clipboard
│   └── theme.toml      # redtail palette + component styles
├── starship.toml
├── swaylock/config
├── yazi/theme.toml
└── systemd/user/
    ├── battery-notify.service
    └── battery-notify.timer
```

Shell files in `$HOME`:
- `.zshrc` — minimal, loads grml-zsh-config
- `.zshrc.local` — PATH, history, aliases, plugins, starship init
- `.zprofile` — cursor env vars

Desktop entries:
- `~/.local/share/applications/spotify-player.desktop` — launches `foot -e spotify_player` (for fuzzel detection)

Custom scripts:
- `~/.local/bin/battery-notify` — battery threshold notifications (20%, 15%, 10%, 5%)

**Backup directories** (`.bak` suffix) exist for dunst, foot, fuzzel, niri, swaylock, waybar — these are pre-rice originals. Don't touch them.

## Dotfile Management — yadm

- **Tool:** yadm 3.5.0 (bare git repo, no symlinks — tracks files in-place)
- **Remote:** `git@github.com:vvaxis/redtail-dotfiles.git` (branch: master)
- **Commit history:**
  - `e30eb75` — micro redtail colorscheme, cursor fix to phinger-cursors-dark
  - `2c61216` — redtail v3: warm palette, ricing, system hardening
  - `c14784e` — primeiro setup
  - `5d8e05a` — initial redtail dotfiles

**Tracked files** (52 files total): all config files listed above (including spotify-player, ignis modules/scripts, systemd units), plus `.zshrc`, `.zshrc.local`, `.zprofile`, `~/.local/bin/battery-notify`, and `~/.local/share/applications/spotify-player.desktop`.

When making changes to dotfiles, **do not run yadm commit** unless the user explicitly asks. The user manages commits himself.

---

## The Rice

### What It Is

Redtail is a warm, dark desktop themed around amber, terracotta, and deep brown — colors drawn from the wallpaper, a digital painting of two silhouetted figures on a riverbank at sunset, with a bridge and city skyline glowing in amber and orange behind them. The name "redtail" is the machine's hostname and the identity of the entire aesthetic.

### What It Aims For

**Warmth over coolness.** The default dark themes in Linux tooling skew blue-gray or neutral charcoal. Redtail rejects this entirely. Every surface — terminal backgrounds, bar pills, notification frames, lock screen rings, editor gutters — is tinted brown. Not gray-that-is-technically-warm. Brown. The user's standard for this is perceptual, not colorimetric: if it looks gray on his screen at his brightness, it is gray, and it needs to be browner.

**Cohesion across every surface.** A rice fails if the palette only lives in small accent elements (a colored border, a bar highlight) while the large surfaces — terminal, browser, file manager — remain default dark gray. Redtail's palette is propagated to 9+ config files. The wallpaper bleeds through transparent terminals and the bar. Every app the user interacts with daily should feel like it belongs to the same environment.

**Transparency as connective tissue.** The single highest-impact change in the rice was terminal alpha. The wallpaper's warmth comes through every terminal window, which simultaneously:
- Connects the wallpaper to the UI (it stops being a hidden background)
- Softens the hard edges between app surfaces
- Makes the brown palette feel organic rather than painted-on

Transparency is used deliberately, not gratuitously: 75% on terminals (`alpha=0.75` in foot), 75% on GTK3 app backgrounds (Nemo — via `rgba()` in gtk-3.0/gtk.css; GTK4/libadwaita apps can't do this due to opaque region), 90% on inactive windows (compositor-level dim), 90% on dashboard cards, 93% on fuzzel, 10% on dunst. btop uses `theme_background = false` to inherit terminal transparency rather than drawing its own. spotify-player also inherits terminal transparency (no `background` in its theme palette).

**Minimalism with substance.** The desktop is clean but not empty. The Ignis sidebar provides real system info (CPU, memory, network, battery, Bluetooth state). The Ignis dashboard (Mod+D) overlays calendar, events, weather, notes, and media controls. The lock screen shows time and date inside a clear indicator ring. Nothing is decoration-only — but nothing is ugly or utilitarian either.

**Personality without gimmicks.** The aesthetic leans melancholic-warm. The wallpaper sets the mood: urban, contemplative, golden hour. The accent color is amber (#d4a243), not neon. The prompt arrow is `▸`, not a spaceship. The font is Iosevka — narrow, technical, no-nonsense. There are no rounded floating bars, no blur-everything compositing effects, no anime waifus. The rice has a clear visual voice without being loud.

### How It Gets There

**The Redtail Palette v0.5:**

| Role | Hex | Where |
|---|---|---|
| Base (background) | `#0e0907` | Terminals, dashboard cards, notifications, GTK content areas, editor, launcher, lock screen |
| Surface (elevated) | `#3f1f13` | Sidebar bg, selections, headerbar, cursor-line, hovered rows, GTK sidebar, cards, dialogs |
| Overlay (borders) | `#745234` | Borders, inactive ring, gutter, indent guides, bright-black |
| Text (cream) | `#e4d7c2` | Primary foreground everywhere |
| Subtext (muted) | `#b6a285` | Secondary text, inactive, placeholder |
| Muted brown | `#6c5745` | Comments, autosuggestions, cmd duration |
| **Amber** (primary accent) | `#d6a241` | Focus ring, statusline, active tab, prompt, match highlight, keywords |
| Bright amber | `#e1b65a` | Directories, types, secondary accent, caps-lock ring |
| Terracotta | `#cb5e3d` | Hostname, identifiers, boolean, video files, backspace highlight |
| Green | `#79ba58` | Strings, git ok, copied, selection mode, Node.js |
| Red | `#ca4949` | Errors, deletions, critical battery, wrong password |
| Blue | `#639cce` | PDFs, underlined, CPU module, Bluetooth |
| Lavender | `#b166c0` | Constants, images, WirePlumber module |
| Teal | `#4fafac` | Special tokens, network module |
| Bright variants | see foot.ini | `#d57070`, `#9dc987`, `#8cb5d8`, `#c38cce`, `#7dbfbc` |

**Palette history:** v0.1/v0.2 used `#1a1714` / `#2a2420` / `#3d352e` as dark anchors — read as gray. v0.3 shifted warmer: `#2a1f14` / `#3b2d1e` / `#4d3b28` — still too desaturated at low brightness, read as cold brown. v0.4 initially pushed both saturation AND lightness to L=16/25/33%, S=45/42/38% — but the user found base too bright. v0.4 was then re-tuned: base pushed very dark (`#150a04`, L=5%, S=68% — deep espresso), surface pulled to `#392214` (L=15%, S=50%). Overlay kept at `#745234`. Accent colors kept their bolder saturation from v0.4: green 25→42%, blue 37→52%, teal 22→38%, lavender 30→42%.

v0.5 addressed the "sea of brown" problem: all three dark anchors at the same hue/saturation made GTK apps feel monotonously brown. Fix: base desaturated and darkened to near-black (`#0e0907`, L=3%, S=35%) — too dark for hue to register visually, reads as "warm darkness." Surface shifted redder and slightly more saturated (`#3f1f13`, H=16°, S=54%, L=16%) — gives "redtail" character to elevated chrome. Overlay unchanged. The key insight: base covers ~60% of GTK pixels (content area), so desaturating it alone massively reduces perceived brown while keeping surface/overlay intentionally warm. Tested by desaturating surface/overlay instead (lost identity, became "brownish gray") and by adding cool accent colors to structural elements (blue scrollbar, green switches — looked alien on warm surfaces). Both approaches failed. Only the base change worked.

Palette is defined in `~/Projects/ricing/palette.conf` and propagated to all configs via `recolor.sh` (see Recolor System below).

**Niri window management:** 15px gaps, 8px corner radius, no borders (off), focus ring 3px in amber/overlay. Shadows are subtle: softness 20, spread 3, y-offset 5. Spread was reduced from 8 because it caused shadows to merge between adjacent windows ("dark haze" effect). Inactive windows at 90% opacity (compositor dim — subtle darkening without revealing wallpaper on opaque apps).

**Key bindings philosophy:** Vim-style (hjkl) alongside arrow keys for all navigation. Mod+Z for terminal (not Mod+Return — Z is closer to the left hand). Mod+Tab for launcher. Mod+A for browser. Single-key launchers for frequently used TUI apps: Mod+G (btop), Mod+Y (yazi), Mod+S (spotify-player). Mod+Shift+C opens niri config in $EDITOR. Media/brightness keys work while locked.

**Niri environment variables:** Daily-driver programs are referenced via shell variables in `spawn-sh` commands, defined in niri's `environment` block: `TERMINAL` (foot), `BROWSER` (zen-browser), `FILE_MANAGER` (nemo), `EDITOR` (micro). Changing a single variable updates all keybindings that use it. Programs unlikely to be swapped (fuzzel, swaylock, blueman, ignis) use `spawn` directly.

### Known Limitations and Unfinished Work

- **Yazi folder icons:** Still default blue (baked into yazi icon defaults; `prepend_conds` approach broke icons entirely). Status bar info segments (4K, Top, 1/11) are also hardcoded light blue. Both would need Lua plugins to fix. Deemed not worth the effort.
- **Niri shadow spread > 5:** Causes shadows to merge between adjacent windows. Keep at 3.
- **micro markdown rendering:** Inline code (backticks) uses the same green as headings — could differentiate. Cursor line highlight is barely visible.
- **Niri window borders:** Tested with solid and gradient approaches — solid is redundant with focus ring, gradients look bad. Borders stay off.
- **Zen Browser:** Not themed (browser CSS ricing is its own rabbit hole). Note: niri compositor opacity rules (applied to active windows) caused Zen to appear brown via wallpaper bleed-through — even though the window didn't look visually transparent. A rendering quirk. Those rules were reverted.
- **Libadwaita/GTK4 transparency:** GTK4/libadwaita apps set `wl_surface.set_opaque_region` on the entire window, blocking both compositor opacity AND CSS-level `rgba()` backgrounds (rgba renders wrong colors instead of transparency because it blends against an internal gray surface, not the wallpaper). No user-level workaround exists. CSS `rgba()` background transparency works on GTK3 apps (Nemo, Blueman) because they don't set opaque region on Wayland. Nemo is the primary GUI file manager; Nautilus remains installed only as a dependency of `xdg-desktop-portal-gnome` (required for screencasting).
- **GTK theme:** Rewritten in v0.5 with full `@define-color` coverage (34+ variables in GTK4, 50+ in GTK3) and widget overrides for all interactive states (buttons, entries, scrollbar, switches, checks, progress, selection, hover, focus, tooltips, tabs, backdrop). Headerbar has a 3px amber bottom stripe. Button:checked uses subtle amber tint (not solid fill) to avoid painting toolbars solid yellow.
- **CSS `spacing` error:** GTK4 CSS parser reports "No property named spacing" on ignis startup. The style.css has NO spacing property — error source is unknown (possibly GTK internals). Cosmetic, doesn't affect rendering.

### Color Usage — Stripe System

The "color usage overhaul" was the biggest design change in this session. The palette had 8 rich accent colors but they only appeared in tiny elements (icon tints, header text). The solution: **accent-colored stripes** — solid colored left-edge lines that give each element a strong color identity without overwhelming the warm base.

**Dashboard cards:** Each card has a 4px solid left border stripe in its accent color (amber=calendar, blue=events, teal=weather, green=notes, lavender=music) + semi-transparent base background (`alpha(#0e0907, 0.90)`). This replaced the barely-visible 2px borders at 45% alpha.

**Sidebar modules:** Each module has an `inset box-shadow 3px` left stripe in its accent color (blue=CPU, yellow=RAM, lavender=volume, amber=brightness, teal=network, blue=bluetooth, green=battery). Module `border-radius` is 0 (straight lines — rounded looked chunky). Module values are 14px bold.

**What was tried and rejected:**
- Transparent alpha accent backgrounds on sidebar modules — looked washed out and ugly
- Font-rendered power icon (`⏻` label) — pushed sidebar wider, couldn't constrain
- `border-left` on sidebar modules — added width even with box-shadow workaround attempts; `inset box-shadow` was the solution (zero layout impact)

**Dunst notifications:** Per-urgency colored frames — green (low/informational), amber (normal), red (critical). Font 14px, slightly larger size (width 220-420, dynamic height 0-180, offset 20x20). Position: top-right.

**Fuzzel launcher:** Amber border (`#d6a241`), font 14px, anchored top-left next to the sidebar (x-margin=30, y-margin=15, 28 lines). Feels like a natural extension of the sidebar.

**btop:** Improved readability — main_fg bumped from subtext to text, graph_text from muted to subtext, box outlines to uniform subtext. Per-box accent-colored outlines were tried but looked noisy with ASCII box-drawing characters — reverted to uniform.

**Niri window borders:** Gradient borders (amber fading to transparent) were tried but looked bad — the gradient smears across the perimeter instead of reading as a clean stripe. Borders stay off; the focus ring (3px amber/overlay) is sufficient.

**What doesn't work for stripes:**
- btop box outlines — ASCII box-drawing characters are too noisy for multi-color treatment
- Niri window borders — uniform on all 4 sides, no per-side support; gradients look bad
- Fuzzel — no per-side border support (rofi has this, but fuzzel is lighter and preferred for 6GB RAM)

### Ignis Dashboard

Both sidebar and dashboard run in a single Ignis process, sharing one CSS file (`~/.config/ignis/style.css`). The dashboard is toggled via `Mod+D` which runs `ignis toggle-window ignis-dashboard`. EWW has been fully removed — all scripts now live in `~/.config/ignis/scripts/`.

**Dashboard window:** Non-anchored overlay layer (no full-screen backdrop). The window sizes to its content and floats centered — clicks outside the cards pass through to windows below. Keyboard events are handled via a `Gtk.EventControllerKey` on the window. Escape closes the dashboard.

**Dashboard modules** (`~/.config/ignis/modules/dashboard/`):
- `calendar.py` — Pure Python calendar grid with Portuguese month names, day selection callback, full keyboard navigation (arrows/hjkl for days, Page Up/Down for months, `t` for today)
- `events.py` — Google Calendar events via `gcal-events.py` script (async via ThreadTask). In-memory cache: today never expires (session lifetime), other days 5min TTL. Clicking an event row opens it in Google Calendar via `xdg-open`.
- `weather.py` — Open-Meteo API (free, no key needed). Poll every 15min + immediate fetch on startup. Location auto-detected via IP geolocation (`ipinfo.io`), with `~/.config/dashboard/location` as optional manual override. Provides true hourly data and proper daily min/max.
- `notes.py` — Direct file read of `~/.local/share/dashboard/notes.md` (Poll every 5s, click opens foot+micro)
- `music.py` — MprisService integration (player_added signal, closed signal on individual players)
- `dashboard.py` — Main orchestrator: two-panel layout (left: calendar+events, right: weather+notes+music). Wires keyboard controller.

**Dashboard scripts** (`~/.config/ignis/scripts/`):
- `weather.py` — Open-Meteo fetcher with WMO code → Nerd Font icon mapping, Portuguese condition descriptions, IP geolocation
- `gcal-events.py` — Google Calendar API fetcher (uses `.venv/` for google-api-python-client). Returns event time, title, and htmlLink.
- `.venv/` — Python 3.14 virtualenv with Google Calendar API dependencies
- `requirements.txt` — pip dependencies for the venv

**Sidebar interactivity:**
- Volume module: right-click opens pwvucontrol
- CPU/RAM modules: click opens btop in foot terminal
- Network/Bluetooth modules: show "on"/"off" labels below icons, colored per module accent (teal/blue when on, muted when off)

**GTK4 renderer fix:** GTK4 4.20+ defaults to Vulkan on Wayland, which causes text clipping artifacts with Iosevka Nerd Font on AMD Radeon Lucienne (fractional pixel glyph positioning). Fix: Ignis is spawned with `GSK_RENDERER=cairo` in niri config. Additionally, `gtk-hint-font-metrics=true` is set in `~/.config/gtk-4.0/settings.ini`.

**Key Ignis/GTK4 gotchas:**
- GTK4 CSS has NO `spacing` property — use `spacing=N` on Widget.Box in Python
- GTK4 CSS has NO `cursor` property
- `Widget.Window(popup=True)` dismisses on ANY click including children — use `popup=False` and close via `ignis toggle-window`
- `Widget.Window(anchor=[all edges])` captures all input even on transparent areas — remove anchors for click-through
- Window backgrounds need explicit `background: transparent` CSS, scoped via `css_classes` to avoid affecting other windows
- MprisService signals use underscores (`player_added`), individual players emit `closed`
- `set_size_request(width, -1)` for fixed widths since CSS `max-width` doesn't work
- `ThreadTask(target=fn, callback=fn)` does NOT auto-run — must call `.run()` explicitly
- ThreadTask callback receives 1 argument (result), not 2
- GTK4 Vulkan/NGL renderer clips text on AMD iGPUs — use `GSK_RENDERER=cairo` for Ignis
- GTK4 focus ring on buttons: suppress with `.day-cell:focus-visible { outline: none; }` when custom selection styling exists

### spotify-player

**What it is:** Rust-based Spotify TUI client (`spotify-player` AUR package). Lightweight (~30 MB RSS), supports sixel album art in Foot, Spotify Connect (acts as a device), MPRIS for Ignis dashboard integration, and lyrics display. Requires Spotify Premium.

**Config location:** `~/.config/spotify-player/` — `app.toml` (behavior/layout), `theme.toml` (colors/styles). No custom keymap — user uses default keybindings ("normie keys", not vim).

**Launch:** `Mod+S` in niri (spawns `foot -e spotify_player`). Also available via fuzzel through the `.desktop` file at `~/.local/share/applications/spotify-player.desktop`.

**Theme philosophy:** Uses the full redtail palette with intentional color roles, not "marrom puro" (all-brown). Each color has a semantic function:
- **Amber** (`bright_yellow` / `BrightYellow`): identity — block titles, table headers
- **Green**: active state — playback status, current playing, progress bar
- **Blue**: informational — artist names
- **Lavender** (`magenta` / `Magenta`): decorative — borders
- **Red**: emotional — liked tracks
- **Surface** (`#3f1f13`): elevated — selections, progress bar unfilled

**Key design decisions:**
- No `background` or `black` in theme palette → inherits Foot terminal transparency (0.75 alpha)
- `border_type = "Rounded"` — consistent with niri corner radius aesthetic
- `progress_bar_type = "Line"` — clean, not block-based
- Cover art at default size (9x5, height 6) — larger sizes created a gap between art and progress bar
- `enable_notify = false` — dunst handles notifications via MPRIS, no double-notify
- `sort_artist_albums_by_type = true` — albums/singles/EPs separated

**Not in recolor.sh:** spotify-player theme uses palette hex values directly but is NOT tracked by the recolor system (it uses TOML color name references like `"Green"`, `"Magenta"` mapped to the `[themes.palette]` section, so only the palette block would need updating on color changes).

### Reference Material

`references/unixporn/` contains ~17 screenshot references from r/unixporn. These are broadly inspirational rather than direct targets. Notable patterns across them:
- Warm sunset/amber palettes with transparent terminals over painted wallpapers (closest to redtail's direction)
- Niri-specific setups showing scrollable tiling with eww overlays and vertical bars
- Brazilian rices with earthy terracotta tones and ASCII art

`guides/` exists but is currently empty.

`CONVERSATION_CONTEXT.md` contains a full recap of all previous Claude Code sessions — bug fixes, audit, ZSH setup, and the entire ricing process with rationale for every decision.

## Recolor System

Palette colors are defined once in `~/Projects/ricing/palette.conf` and propagated to all 13 color-bearing config files via in-place sed replacement.

### Files

```
~/Projects/ricing/
├── palette.conf        # source of truth — 20 named colors, bare hex (no #)
├── .palette.current    # snapshot of hex values currently in the configs
└── recolor.sh          # reads both, swaps old → new across all config files
```

### How it works

1. Edit a color in `palette.conf` (e.g., `amber=d4a243` → `amber=e0a030`)
2. Run `./recolor.sh`
3. The script compares `palette.conf` against `.palette.current`, finds changed values, and does a two-pass sed replacement (old hex → temporary token → new hex) to avoid cascading when colors swap values
4. All 13 config files are updated in-place, `.palette.current` is updated

### Config files touched (13)

foot.ini, dunstrc, fuzzel.ini, niri/config.kdl, gtk-3.0/gtk.css, gtk-4.0/gtk.css, swaylock/config, starship.toml, yazi/theme.toml, micro/colorschemes/redtail.micro, btop/themes/redtail.theme, .zshrc.local, ignis/style.css

### Important

- Configs remain the source of truth for everything except colors. Edit them directly for non-color changes.
- `palette.conf` stores bare hex without `#`. The `#` prefix, alpha suffixes (`ee`, `ff`, `dd`, `00`), and quoting are part of each config's own syntax and are not touched by the script.
- Non-palette colors (`#00001a`/`#00000050` shadows in niri, `00000000` separator in swaylock) are not in palette.conf and are never touched.
- `rgba()` values in GTK CSS files use RGB components of the base color (e.g., `rgba(14, 9, 7, 0.36)` for `#0e0907`). These are NOT updated by `recolor.sh` and require manual adjustment if the base changes.
- yadm tracks both the generated configs at `~/.config/` and the recolor system itself (`palette.conf`, `.palette.current`, `recolor.sh`).

---

## Working on This Project

### Rules

1. **Read before editing.** Never propose changes to a config you haven't read.
2. **Check dependencies before removing packages.** Always run `pactree -r <pkg>` first.
3. **Don't commit.** The user manages yadm commits himself. Only commit if explicitly asked.
4. **Don't revert user choices.** Inactive window opacity at 0.90, foot alpha at 0.75, GTK3 rgba backgrounds — all intentional. phinger-cursors-dark is the cursor. `add_newline = false` in starship is deliberate. If a setting seems aggressive, it was probably discussed and chosen.
5. **Palette changes go through recolor.sh.** Edit `palette.conf`, run `./recolor.sh`. Do not manually edit hex values across configs — the script handles all 13 files. See Recolor System below.
6. **Perception over theory.** If the user says a color looks gray, it's gray. Don't argue that it's "technically warm" by hex value.
7. **RAM awareness.** The machine has 6 GB. Don't suggest always-on daemons or memory-heavy tools without accounting for this.
8. **Test shadows conservatively.** Niri shadow spread should not exceed 5.
9. **Ignis CSS reloads instantly.** No need to restart ignis for CSS-only changes. Only restart for Python module changes.
10. **grml overrides starship.** The `prompt off` line in `.zshrc.local` before `eval "$(starship init zsh)"` is required. Don't remove it.

### Palette Quick Reference (v0.5)

```
Base       #0e0907    Surface    #3f1f13    Overlay    #745234
Text       #e4d7c2    Subtext    #b6a285    Muted      #6c5745
Amber      #d6a241    Yellow     #e1b65a    Terracotta #cb5e3d
Green      #79ba58    Red        #ca4949    Blue       #639cce
Lavender   #b166c0    Teal       #4fafac
```

---

## Pending Tasks

### GTK Theme Rethink — DONE (v0.5)

Rewritten with full variable coverage and widget overrides. The "sea of brown" was solved by palette v0.5: near-black base for content areas, warm red-brown surface for chrome. Both GTK3 and GTK4 files now have 34+ `@define-color` variables (including all shade, scrollbar, destructive, headerbar variables that libadwaita reads) and interactive widget overrides (buttons, entries, scrollbar, switches, checks, progress, selection, hover, focus, tooltips, tabs, backdrop).

Remaining notes:
- Zen Browser (GTK3) proved resistant to `gtk-3.0/gtk.css` changes — may need separate approach.
- libadwaita apps respect `@define-color` variables but not direct widget overrides — the variables alone cover most visual needs.

### GTK App Transparency — DONE (GTK3 only)

GTK3 apps (Nemo, Blueman) have CSS-level background transparency via `rgba(14, 9, 7, 0.75)` in `gtk-3.0/gtk.css`. This works because GTK3 on Wayland doesn't set `wl_surface.set_opaque_region`.

GTK4/libadwaita apps (Nautilus) cannot have transparency — they set opaque region AND CSS `rgba()` blends against an internal surface instead of the wallpaper, producing wrong colors. Nautilus remains installed as a dependency of `xdg-desktop-portal-gnome` (portal-gnome provides ScreenCast for screen sharing; replacing with portal-gtk + portal-wlr is possible but risky since portal-wlr is designed for wlroots, not Smithay/niri). Nemo is the daily-driver file manager.

Inactive windows use compositor opacity at 0.90 (niri `match is-active=false`) — subtle dim without revealing wallpaper on opaque apps. Active-window compositor opacity was tested and **should not be re-added** — it caused text transparency on all apps and a rendering quirk on Zen Browser.
