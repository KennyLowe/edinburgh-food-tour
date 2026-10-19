# The Edinburgh Edit

A responsive static Edinburgh food-tour planner, ending at Gaucho Edinburgh. Seven timed stops, interactive OpenStreetMap pins, walking directions, optional detours, expandable practical notes and a print stylesheet. No bookings, purchases, trackers, API keys, JavaScript or build dependencies.

## Preview

Run `python3 -m http.server 8080` from this directory; open http://localhost:8080.

## GitHub Pages

The root contains the ready-to-publish site. All local URLs are relative, so the app works beneath `/edinburgh-food-tour/`. `.nojekyll` bypasses Jekyll. Publish the root of main through the separate authorized publication workflow. Development does not enable Pages or change repository visibility.

## Content

Times, walking distances and budgets are planning estimates, not verified live availability. Check venues directly for current hours, menus, accessibility and reservations. Nothing is booked. Stop markers are approximate. Google Maps may omit waypoints on some mobile clients; individual directions links are included.

The core itinerary works without scripts or third-party requests. Online maps and optional Google Fonts require connectivity; system fonts are fallbacks. OpenStreetMap attribution is provided within its embed. The skyline is an original SVG illustration, not a photograph or geographic map.

Use the browser's Print command for a clean full itinerary. Practical notes are initially expanded; reopen any collapsed notes before printing if you want them included.

## Verification

`python3 check_site.py` validates site structure, map URLs, itinerary order, local files and project-subpath HTTP serving. This is not a visual browser test or live venue validation.
