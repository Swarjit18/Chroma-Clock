import js
import time
from pyodide.ffi import create_proxy
from pyscript import document

# --- Global State ---
alarms = [
    {"time": "06:30", "label": "Morning Workout", "active": True},
    {"time": "08:00", "label": "Breakfast", "active": False}
]

sw_running = False
sw_start_time = 0
sw_elapsed = 0

current_locale = "local"
current_timezone = "local"

# --- Live Clock & Stopwatch Engine ---
def update_time():
    now = js.Date.new()
    
    if current_locale == "local":
        time_str = now.toLocaleTimeString()
        date_str = now.toLocaleDateString(js.undefined, {"weekday": "long", "month": "long", "day": "numeric"})
    else:
        options_time = {"timeZone": current_timezone, "hour": "2-digit", "minute": "2-digit", "second": "2-digit"}
        options_date = {"timeZone": current_timezone, "weekday": "long", "month": "long", "day": "numeric"}
        time_str = now.toLocaleTimeString(current_locale, **options_time)
        date_str = now.toLocaleDateString(current_locale, **options_date)
        
    document.querySelector("#liveClockDisplay").innerText = time_str
    document.querySelector("#liveDateDisplay").innerText = date_str

    global sw_elapsed
    if sw_running:
        sw_elapsed = time.time() - sw_start_time
        display_stopwatch()

def display_stopwatch():
    total_ms = int(sw_elapsed * 1000)
    hours = total_ms // 3600000
    minutes = (total_ms % 3600000) // 60000
    seconds = (total_ms % 60000) // 1000
    ms = (total_ms % 1000) // 10
    
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:02d}"
    if hours == 0:
        time_str = f"{minutes:02d}:{seconds:02d}.{ms:02d}"
        
    document.querySelector("#stopwatchTime").innerText = time_str

# Start background ticker
js.setInterval(create_proxy(update_time), 50)


# --- Alarm Logic ---
def render_alarms():
    container = document.querySelector("#alarmList")
    container.innerHTML = ""
    
    if not alarms:
        container.innerHTML = "<div class='empty-state'>No alarms configured.</div>"
        return
        
    for i, alarm in enumerate(alarms):
        active_cls = "active" if alarm["active"] else ""
        card_dim = "" if alarm["active"] else "dimmed"
        
        h, m = map(int, alarm['time'].split(':'))
        ampm = "PM" if h >= 12 else "AM"
        display_h = h % 12
        if display_h == 0: display_h = 12
        display_time = f"{display_h:02d}:{m:02d} {ampm}"
        
        card = document.createElement("div")
        card.className = "alarm-card"
        card.innerHTML = f"""
            <div class="alarm-info {card_dim}">
                <div class="alarm-time">{display_time}</div>
                <div class="alarm-label">{alarm['label']}</div>
            </div>
            <div class="alarm-actions">
                <button class="icon-btn delete-btn" data-idx="{i}">🗑️</button>
                <div class="toggle-switch {active_cls}" data-idx="{i}">
                    <div class="toggle-knob"></div>
                </div>
            </div>
        """
        container.appendChild(card)

# Bind delete and toggle switches
def handle_alarm_clicks(e):
    target = e.target
    
    del_btn = target.closest(".delete-btn")
    if del_btn:
        idx = int(del_btn.getAttribute("data-idx"))
        alarms.pop(idx)
        render_alarms()
        return
        
    toggle = target.closest(".toggle-switch")
    if toggle:
        idx = int(toggle.getAttribute("data-idx"))
        alarms[idx]["active"] = not alarms[idx]["active"]
        render_alarms()
        return

document.querySelector("#alarmList").addEventListener("click", create_proxy(handle_alarm_clicks))

def open_add_alarm(e):
    document.querySelector("#newAlarmTime").value = "07:00"
    document.querySelector("#newAlarmLabel").value = ""
    document.querySelector("#alarmModal").classList.add("show")

def close_add_alarm(e):
    document.querySelector("#alarmModal").classList.remove("show")

def save_alarm(e):
    time_val = document.querySelector("#newAlarmTime").value
    label_val = document.querySelector("#newAlarmLabel").value.strip()
    if not time_val: return
    if not label_val: label_val = "Alarm"
    
    alarms.append({"time": time_val, "label": label_val, "active": True})
    alarms.sort(key=lambda x: x['time'])
    
    close_add_alarm(e)
    render_alarms()


# --- Stopwatch Logic ---
def toggle_stopwatch(e):
    global sw_running, sw_start_time
    btn = document.querySelector("#swToggleBtn")
    
    if sw_running:
        sw_running = False
        btn.innerText = "Resume"
        btn.classList.remove("sw-pause")
        btn.classList.add("sw-start")
    else:
        sw_running = True
        sw_start_time = time.time() - sw_elapsed
        btn.innerText = "Pause"
        btn.classList.remove("sw-start")
        btn.classList.add("sw-pause")

def reset_stopwatch(e):
    global sw_running, sw_elapsed
    sw_running = False
    sw_elapsed = 0
    display_stopwatch()
    btn = document.querySelector("#swToggleBtn")
    btn.innerText = "Start"
    btn.classList.remove("sw-pause")
    btn.classList.add("sw-start")


# --- Navigation & Settings ---
def switch_tab(e):
    target_btn = e.target.closest(".nav-btn")
    if not target_btn: return
    
    for btn in document.querySelectorAll(".nav-btn"):
        btn.classList.remove("active")
    target_btn.classList.add("active")
    
    target_id = target_btn.getAttribute("data-target")
    for tab in document.querySelectorAll(".tab-content"):
        tab.classList.remove("active")
    document.querySelector(f"#{target_id}").classList.add("active")

def toggle_menu(e):
    document.querySelector("#settingsMenu").classList.toggle("show")

def set_light_theme(e):
    document.body.classList.remove("theme-dark")
    document.body.classList.add("theme-light")
    toggle_menu(e)

def set_dark_theme(e):
    document.body.classList.remove("theme-light")
    document.body.classList.add("theme-dark")
    toggle_menu(e)

def change_clock_style(e):
    select = document.querySelector("#clockStyleSelect")
    style_val = select.value
    document.body.classList.remove("clock-standard", "clock-digital", "clock-minimal")
    document.body.classList.add(f"clock-{style_val}")
    toggle_menu(e)

def change_region(e):
    global current_locale, current_timezone
    val = document.querySelector("#regionSelect").value
    if val == "local":
        current_locale = "local"
        current_timezone = "local"
    else:
        current_locale, current_timezone = val.split(",")
    toggle_menu(e)

# Initial Setup
render_alarms()
update_time()