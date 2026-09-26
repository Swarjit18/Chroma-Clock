ChromaClock is a modern, responsive, client-side timekeeping and alarm application built with HTML, CSS, and Python. Powered by the PyScript framework, the application runs entirely in the browser without requiring a backend server.

Features
Browser-Native Python: Uses PyScript to execute Python logic directly in the client browser.

Live Regional Clock: Displays the current time and date, with support for switching between local time and various international time zones (EST, GMT, JST, IST).

Alarm Management: Add, toggle, and delete alarms using a clean, interactive UI.

Precision Stopwatch: A built-in stopwatch featuring start, pause, and reset controls that track time down to the millisecond.

Dynamic Theming: Instantly toggle between a sleek Dark Theme and a vibrant Light Theme via the settings menu.

Customizable Typography: Choose between Standard, Digital LED, and Minimal clock styles to suit your aesthetic preferences.

File Structure
The project relies on a single-page architecture split across three core files:

index.html: The structural foundation, featuring a mobile-inspired layout, navigation tabs, a glassmorphism modal, and a <py-config> block designed to safely load the Python engine.

main.py: The application logic. It manages a 50ms interval ticker for the clock and stopwatch, handles state arrays for alarm management, and interacts directly with the HTML DOM via PyScript's proxy elements.

style.css: The visual design layer, utilizing CSS variables, flexbox, grid, and smooth transitions to create an elegant user experience.
