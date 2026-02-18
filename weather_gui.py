import customtkinter as ctk
from weather_api import geocode_location, get_weather_forecast


# --- App window setup -------------------------------------------------
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

weather_app = ctk.CTk()
weather_app.geometry("600x700")
weather_app.title("Family Weather Dashboard")

title_label = ctk.CTkLabel(
    weather_app,
    text="Family Weather Dashboard",
    font=("Segoe UI", 22, "bold")
)
title_label.pack(pady=(20, 10))


# --- Location inputs (side‑by‑side A and B) ---------------------------
locations_frame = ctk.CTkFrame(weather_app)
locations_frame.pack(padx=10, pady=10, fill="x")
locations_frame.grid_columnconfigure((0, 1), weight=1)

location_label_a = ctk.CTkLabel(
    locations_frame,
    text="Location A: (e.g. 60601, Chicago, IL)"
)
location_label_a.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

location_input_a = ctk.CTkEntry(locations_frame, width=250, height=40)
location_input_a.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")

location_label_b = ctk.CTkLabel(
    locations_frame,
    text="Location B: (e.g. 80204, Denver, CO)"
)
location_label_b.grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")

location_input_b = ctk.CTkEntry(locations_frame, width=250, height=40)
location_input_b.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="ew")


# --- Presets / controls (show full, quick pairs, flip) ----------------
presets_frame = ctk.CTkFrame(weather_app)
presets_frame.pack(padx=10, pady=(0, 10))

# full vs 1‑day toggle
show_full_forecast = ctk.BooleanVar(value=True)
toggle_full_forecast = ctk.CTkCheckBox(
    presets_frame,
    text="Show full forecast",
    variable=show_full_forecast,
)
toggle_full_forecast.pack(side="left", padx=5)


def set_home_vs_denver():
    """Preset: Appleton vs Englewood and fetch both."""
    location_input_a.delete(0, "end")
    location_input_a.insert(0, "54913")
    location_input_b.delete(0, "end")
    location_input_b.insert(0, "80110")
    fetch_both()


def set_home_vs_san_diego():
    """Preset: Appleton vs San Diego and fetch both."""
    location_input_a.delete(0, "end")
    location_input_a.insert(0, "Appleton, WI")
    location_input_b.delete(0, "end")
    location_input_b.insert(0, "San Diego, CA")
    fetch_both()


preset_btn_1 = ctk.CTkButton(
    presets_frame,
    text="Home vs Denver",
    command=set_home_vs_denver,
    width=140
)
preset_btn_1.pack(side="left", padx=5)

preset_btn_2 = ctk.CTkButton(
    presets_frame,
    text="Home vs San Diego",
    command=set_home_vs_san_diego,
    width=140
)
preset_btn_2.pack(side="left", padx=5)


def flip_locations():
    """Swap A and B locations and refresh."""
    a_text = location_input_a.get()
    b_text = location_input_b.get()
    location_input_a.delete(0, "end")
    location_input_a.insert(0, b_text)
    location_input_b.delete(0, "end")
    location_input_b.insert(0, a_text)
    fetch_both()


flip_btn = ctk.CTkButton(
    presets_frame,
    text="Flip A/B Locations",
    command=flip_locations,
    width=120
)
flip_btn.pack(side="left", padx=5)


# --- Outputs (two forecast text areas side‑by‑side) -------------------
outputs_frame = ctk.CTkFrame(weather_app)
outputs_frame.pack(padx=10, pady=10, fill="both", expand=True)
outputs_frame.grid_columnconfigure((0, 1), weight=1)
outputs_frame.grid_rowconfigure(0, weight=1)

weather_output_a = ctk.CTkTextbox(outputs_frame, width=275, height=400)
weather_output_a.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

weather_output_b = ctk.CTkTextbox(outputs_frame, width=275, height=400)
weather_output_b.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


# --- Convenience: focus Location A on startup -------------------------
def focus_location_input():
    location_input_a.focus_set()


weather_app.after(100, focus_location_input)


# --- Core: fetch forecast for one entry + render into one textbox -----
def fetch_weather_for(entry_widget, output_widget, label_prefix=""):
    """Fetch NWS forecast for one location, render to one textbox, and
    return the first period for comparison (today/tonight)."""
    user_input = entry_widget.get()

    output_widget.delete("1.0", "end")
    output_widget.insert("1.0", "📍 Fetching weather data...\n")

    coords = geocode_location(user_input)
    if not coords:
        output_widget.delete("1.0", "end")
        output_widget.insert(
            "end",
            "❌ Location not found...\nTry: 'City, State' or 5-digit zip code"
        )
        return None

    latitude, longitude, resolved_location = coords
    periods = get_weather_forecast(latitude, longitude)
    if not periods:
        output_widget.delete("1.0", "end")
        output_widget.insert("end", "❌ Unable to fetch forecast for this location.\n")
        return None

    output_widget.delete("1.0", "end")
    output_widget.insert(
        "end",
        f"{label_prefix}📍 Forecast for {resolved_location}\n\n"
    )

    periods_to_show = periods[:14] if show_full_forecast.get() else periods[:1]

    for period in periods_to_show:
        text = f"📅 {period['name']}\n"
        text += f"🌡️ {period['temperature']}°{period['temperatureUnit']}\n"
        text += f"☁️ {period['shortForecast']}\n"
        text += f"💨 {period['windSpeed']} out of the {period['windDirection']}\n\n"
        output_widget.insert("end", text)

    return periods[0]


# --- Wrappers: fetch for Location A and B -----------------------------
def fetch_weather_a(event=None):
    return fetch_weather_for(location_input_a, weather_output_a, label_prefix="Location A: ")


def fetch_weather_b(event=None):
    return fetch_weather_for(location_input_b, weather_output_b, label_prefix="Location B: ")


# --- Compare both and inject summary at top ---------------------------
def fetch_both(event=None):
    """Fetch A and B, compare today's temps, and show a summary in both boxes."""
    today_a = fetch_weather_a()
    today_b = fetch_weather_b()

    if not (today_a and today_b):
        return

    temp_a = today_a["temperature"]
    temp_b = today_b["temperature"]
    unit = today_a["temperatureUnit"]

    if temp_a > temp_b:
        summary = f"Today: Location A is {temp_a - temp_b}°{unit} warmer than Location B.\n\n"
    elif temp_b > temp_a:
        summary = f"Today: Location B is {temp_b - temp_a}°{unit} warmer than Location A.\n\n"
    else:
        summary = "Today: Location A & B have the same temperature.\n\n"

    for box in (weather_output_a, weather_output_b):
        box.insert("1.0", summary)


# --- Triggers: Enter key + button ------------------------------------
location_input_a.bind("<Return>", fetch_both)
location_input_b.bind("<Return>", fetch_both)

submit_button = ctk.CTkButton(
    weather_app,
    text="Weather Time!",
    command=fetch_both,
    width=150,
    height=40
)
submit_button.pack(padx=10, pady=20)


# --- Sync scroll: scroll both textboxes with mouse wheel -------------
def sync_mousewheel(event):
    weather_output_a.yview_scroll(int(-1 * (event.delta / 120)), "units")
    weather_output_b.yview_scroll(int(-1 * (event.delta / 120)), "units")
    return "break"


weather_output_a.bind("<MouseWheel>", sync_mousewheel)
weather_output_b.bind("<MouseWheel>", sync_mousewheel)


# --- Run app ----------------------------------------------------------
weather_app.mainloop()