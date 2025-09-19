import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import flet as ft
import logging
from logging.handlers import RotatingFileHandler
import uuid
import os
import json


# ---------- Custom UI Log Handler ----------
class FletLogHandler(logging.Handler):
    """Custom logging handler that writes log records into a Flet ListView."""

    def __init__(self, console_output: ft.ListView, page: ft.Page):
        super().__init__()
        self.console_output = console_output
        self.page = page

    def emit(self, record):
        """Append formatted log record to the ListView if mounted, else skip."""
        msg = self.format(record)
        try:
            if self.console_output.page:
                self.console_output.controls.append(
                    ft.Text(msg, size=12, color=ft.Colors.WHITE)
                )
                self.console_output.scroll_to(offset=1.0, duration=100)
                self.page.update()
        except Exception:
            print(f"[UI Log Fallback] {msg}")
            self.handleError(record)


def configure_logger(console_output: ft.ListView, page: ft.Page) -> logging.Logger:
    """Configure root logger with file + Flet handlers, including OCI SDK loggers."""
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    logger = logging.getLogger("flet_app")
    logger.setLevel(logging.INFO)

    # Formatter styles
    ui_fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    file_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    # UI handler
    ui_handler = FletLogHandler(console_output, page)
    ui_handler.setFormatter(ui_fmt)

    # Rotating file handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(file_fmt)

    if not logger.handlers:
        logger.addHandler(ui_handler)
        logger.addHandler(file_handler)

        # Also attach to OCI SDK loggers
        for name in [
            "oci",
            "oci.identity",
            "oci.identity_domains",
            "oci.generative_ai_inference",
        ]:
            sdk_logger = logging.getLogger(name)
            sdk_logger.setLevel(logging.INFO)
            sdk_logger.addHandler(ui_handler)
            sdk_logger.addHandler(file_handler)

        logger.info("Logger initialized with UI and rotating file handlers.")
    return logger


def main(page: ft.Page):
    """Main entrypoint for the Flet application."""
    page.title = "NavRail App with Login + Console & Detail Fly-in + File Logging"
    page.theme_mode = "light"

    # ---------- SECRET TOKEN ----------
    session_token = str(uuid.uuid4())
    print(f"🔑 Session token (share with user): {session_token}")

    page.session.set("authenticated", False)

    # ---------- Logger Setup ----------
    console_output = ft.ListView(expand=True, auto_scroll=True, spacing=2)
    logger = configure_logger(console_output, page)

    def clear_console(e):
        console_output.controls.clear()
        logger.debug("Console output cleared.")
        page.update()

    clear_btn = ft.ElevatedButton("Clear Console", on_click=clear_console)

    flyin_console = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Console Log", color=ft.Colors.AMBER, expand=True),
                        clear_btn,
                    ]
                ),
                ft.Divider(),
                console_output,
            ]
        ),
        height=200,
        bgcolor=ft.Colors.BLACK,
        visible=False,
    )

    # ---------- Global App State ----------
    app_state = {
        "settings_complete": False,
        "selected_detail": None,
    }

    # ---------- Detail Fly-in ----------
    def close_detail():
        detail_flyin.visible = False
        page.update()

    detail_flyin = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Details", style="headlineSmall", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            tooltip="Close",
                            on_click=lambda e: close_detail(),
                        ),
                    ]
                ),
                ft.Text("Select a row..."),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        width=300,
        bgcolor=ft.Colors.GREY_200,
        visible=False,
        padding=10,
    )

    def show_detail(item: dict):
        """Show JSON detail in fly-in."""
        app_state["selected_detail"] = item
        detail_flyin.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Details", style="headlineSmall", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            tooltip="Close",
                            on_click=lambda e: close_detail(),
                        ),
                    ]
                ),
                ft.Text(json.dumps(item, indent=2), selectable=True),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        detail_flyin.visible = True
        main_area.update()

    # ---------- Fake Data ----------
    sample_policies = [
        {
            "id": f"p{i}",
            "name": f"Policy{i}",
            "statements": [f"ALLOW group G{i} to read resource{i}"],
        }
        for i in range(1, 21)
    ]

    sample_users = [
        {"id": f"u{i}", "name": f"User{i}", "groups": [f"Group{i%3}"]}
        for i in range(1, 31)
    ]

    # ---------- Navigation Buttons (global refs) ----------
    goto_policies_btn = ft.ElevatedButton(
        "Go to Policies", disabled=True, on_click=lambda e: show_page(1)
    )
    goto_users_btn = ft.ElevatedButton(
        "Go to Users", disabled=True, on_click=lambda e: show_page(2)
    )

    # ---------- Pages ----------
    def settings_view():
        status = ft.Text(
            "✅ Settings complete!"
            if app_state["settings_complete"]
            else "Complete settings to unlock other pages",
            color="green" if app_state["settings_complete"] else "red",
        )

        toggle_console = ft.Checkbox(
            label="Show Console Log", value=flyin_console.visible
        )

        log_level_dropdown = ft.Dropdown(
            label="Log Level",
            options=[
                ft.dropdown.Option("DEBUG"),
                ft.dropdown.Option("INFO"),
                ft.dropdown.Option("WARNING"),
                ft.dropdown.Option("ERROR"),
            ],
            value=logging.getLevelName(logger.level),
            width=150,
        )

        def complete_settings(e):
            app_state["settings_complete"] = True
            status.value = "✅ Settings complete!"
            status.color = "green"
            goto_policies_btn.disabled = False
            goto_users_btn.disabled = False
            logger.info("Settings marked complete.")
            main_area.update()

        def toggle_console_log(e):
            flyin_console.visible = e.control.value
            logger.info(
                f"Console log {'enabled' if e.control.value else 'disabled'}."
            )
            page.update()

        def change_log_level(e):
            new_level = getattr(logging, e.control.value)
            logger.setLevel(new_level)
            for name in [
                "oci",
                "oci.identity",
                "oci.identity_domains",
                "oci.generative_ai_inference",
            ]:
                logging.getLogger(name).setLevel(new_level)
            logger.info(f"Log level changed to {e.control.value}")

        toggle_console.on_change = toggle_console_log
        log_level_dropdown.on_change = change_log_level

        return ft.Column(
            [
                ft.Text("Settings Page", style="headlineSmall"),
                ft.Dropdown(
                    label="Tenancy Profile",
                    options=[ft.dropdown.Option("Profile1")],
                ),
                ft.Row([toggle_console, log_level_dropdown]),
                ft.ElevatedButton("Save Settings", on_click=complete_settings),
                status,
                ft.Row([goto_policies_btn, goto_users_btn]),
            ],
            expand=True,
        )

    def policies_view():
        rows = []
        for p in sample_policies:
            row = ft.DataRow(
                cells=[ft.DataCell(ft.Text(p["id"])), ft.DataCell(ft.Text(p["name"]))],
                on_select_changed=lambda e, item=p: show_detail(item),
            )
            rows.append(row)

        return ft.Container(
            content=ft.Column(
                [
                    ft.DataTable(
                        columns=[ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Name"))],
                        rows=rows,
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )


    def users_view():
        rows = []
        for u in sample_users:
            row = ft.DataRow(
                cells=[ft.DataCell(ft.Text(u["id"])), ft.DataCell(ft.Text(u["name"]))],
                on_select_changed=lambda e, item=u: show_detail(item),
            )
            rows.append(row)

        return ft.Container(
            content=ft.DataTable(
                columns=[ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Name"))],
                rows=rows,
            ),
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    # ---------- Content Routing ----------
    content_area = ft.Column(expand=True)

    def locked_message():
        return ft.Container(
            content=ft.Text("⚠️ Please complete Settings first", color="red"),
            alignment=ft.alignment.center,
        )

    def show_page(index: int):
        navrail.selected_index = index
        if index == 0:
            content_area.controls = [settings_view()]
        elif index == 1:
            content_area.controls = (
                [policies_view()]
                if app_state["settings_complete"]
                else [locked_message()]
            )
        elif index == 2:
            content_area.controls = (
                [users_view()]
                if app_state["settings_complete"]
                else [locked_message()]
            )
        main_area.update()

    # ---------- NavRail ----------
    navrail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Settings"),
            ft.NavigationRailDestination(icon=ft.Icons.POLICY, label="Policies"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Users"),
        ],
        on_change=lambda e: show_page(e.control.selected_index),
    )

    # ---------- Layout (detail right, console bottom) ----------
    main_area = ft.Row(
        [navrail, ft.VerticalDivider(width=1), content_area, detail_flyin],
        expand=True,
    )

    layout = ft.Column(
        [
            main_area,   # main area with nav + content + detail
            flyin_console,  # console at bottom
        ],
        expand=True,
    )

    # ---------- Login Overlay ----------
    overlay_bg = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
        expand=True,
        visible=True,
    )

    token_field = ft.TextField(label="Enter session token", width=250)
    login_message = ft.Text("Please enter the token from server logs", color="white")

    def do_login(e):
        if token_field.value.strip() == session_token:
            page.session.set("authenticated", True)
            overlay_bg.visible = False
            login_box.visible = False
            logger.info("User logged in successfully.")
        else:
            login_message.value = "❌ Invalid token, try again"
            logger.warning("Failed login attempt.")
        page.update()

    login_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login Required", style="headlineMedium", color="white"),
                token_field,
                ft.ElevatedButton("Login", on_click=do_login),
                login_message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLUE_GREY_900),
        border_radius=10,
        padding=20,
        alignment=ft.alignment.center,
        visible=True,
    )

    # ---------- Add to Page ----------
    page.add(
        ft.Stack(
            [
                layout,
                overlay_bg,
                login_box,
            ],
            expand=True,
        )
    )

    show_page(0)
    logger.info("App started and initial page displayed.")


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
