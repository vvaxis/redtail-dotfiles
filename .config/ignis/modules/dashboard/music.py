from ignis.widgets import Widget


def music_card() -> Widget.Box:
    try:
        from ignis.services.mpris import MprisService
        has_mpris = True
    except Exception:
        has_mpris = False

    title_label = Widget.Label(
        label="Nenhum player ativo",
        css_classes=["music-title", "music-empty"],
        halign="start",
        ellipsize="end",
        max_width_chars=30,
    )
    artist_label = Widget.Label(
        label="",
        css_classes=["music-artist"],
        halign="start",
        ellipsize="end",
        max_width_chars=30,
        visible=False,
    )

    prev_btn = Widget.Button(
        label="󰒮",
        css_classes=["music-btn"],
        sensitive=False,
    )
    play_btn = Widget.Button(
        label="󰐊",
        css_classes=["music-btn", "music-btn-play"],
        sensitive=False,
    )
    next_btn = Widget.Button(
        label="󰒭",
        css_classes=["music-btn"],
        sensitive=False,
    )

    controls = Widget.Box(
        spacing=16,
        css_classes=["music-controls"],
        halign="center",
        child=[prev_btn, play_btn, next_btn],
    )

    _current_player = {"ref": None}

    def _update_from_player(player=None):
        p = player or _current_player["ref"]
        if p is None:
            title_label.set_label("Nenhum player ativo")
            title_label.set_css_classes(["music-title", "music-empty"])
            artist_label.visible = False
            play_btn.set_label("󰐊")
            prev_btn.sensitive = False
            play_btn.sensitive = False
            next_btn.sensitive = False
            return

        title = getattr(p, "title", "") or ""
        artist = getattr(p, "artist", "") or ""
        status = getattr(p, "playback_status", "Stopped") or "Stopped"

        title_label.set_label(title if title else "Nenhum player ativo")
        title_label.set_css_classes(
            ["music-title"] if title else ["music-title", "music-empty"]
        )

        if artist:
            artist_label.set_label(artist)
            artist_label.visible = True
        else:
            artist_label.visible = False

        play_btn.set_label("󰏤" if status == "Playing" else "󰐊")
        prev_btn.sensitive = True
        play_btn.sensitive = True
        next_btn.sensitive = True

    def _on_player_closed(player):
        if _current_player["ref"] is player:
            _current_player["ref"] = None
            # Try to fall back to another player
            players = mpris.players if has_mpris else []
            if players:
                _bind_player(players[0])
            else:
                _update_from_player(None)

    def _bind_player(player):
        _current_player["ref"] = player
        player.connect("notify::title", lambda *_: _update_from_player(player))
        player.connect("notify::artist", lambda *_: _update_from_player(player))
        player.connect("notify::playback-status", lambda *_: _update_from_player(player))
        player.connect("closed", lambda p: _on_player_closed(p))
        _update_from_player(player)

        prev_btn.on_click = lambda _b: player.previous()
        play_btn.on_click = lambda _b: player.play_pause()
        next_btn.on_click = lambda _b: player.next()

    if has_mpris:
        mpris = MprisService.get_default()

        def _on_player_added(service, player):
            _bind_player(player)

        mpris.connect("player_added", _on_player_added)

        # Bind to existing player if any
        if mpris.players:
            _bind_player(mpris.players[0])

    return Widget.Box(
        vertical=True,
        css_classes=["card", "music-card"],
        child=[
            Widget.Label(
                label="󰎈  Música",
                css_classes=["section-header"],
                halign="start",
            ),
            Widget.Box(
                vertical=True,
                spacing=10,
                css_classes=["music-content"],
                child=[
                    title_label,
                    artist_label,
                    controls,
                ],
            ),
        ],
    )
