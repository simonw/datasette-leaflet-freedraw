DATASETTE_TILE_LAYER = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
DATASETTE_TILE_LAYER_OPTIONS = {
  maxZoom: 19,
  detectRetina: true,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
};

window.addEventListener("load", () => {
  let inputs = [
    ...document.querySelectorAll("input[name=freedraw]"),
    ...document.querySelectorAll("input[name$=_freedraw]"),
  ];
  inputs.forEach(configureMap);
});

function configureMap(input) {
  let div = document.createElement("div");
  div.style.marginTop = "1em";
  div.style.height = "350px";
  input.parentElement.appendChild(div);
  let tiles = L.tileLayer(DATASETTE_TILE_LAYER, DATASETTE_TILE_LAYER_OPTIONS);
  let map = L.map(div, {
    center: L.latLng(0, 0),
    zoom: 2,
    layers: [tiles],
  });
  let freeDraw = new FreeDraw();
  /* If input.value is GeoJSON, add those to the map */
  let allPoints = [];
  try {
    let existing = JSON.parse(input.value);
    if (existing.type == "MultiPolygon") {
      window.existing = existing;
      map.addLayer(freeDraw);
      existing.coordinates.forEach(([outers, inners]) => {
        let points = outers.map(
          ([longitude, latitude]) => new L.LatLng(latitude, longitude)
        );
        freeDraw.create(points);
        allPoints.push(...points);
      });
      map.fitBounds(allPoints);
    }
  } catch (e) {}
  if (!allPoints.length) {
    // Map starts in pan-zoom mode
    let controls = document.createElement("div");
    input.parentElement.appendChild(controls);
    let button = document.createElement("button");
    // This prevents button from being activated on form submit:
    button.setAttribute("type", "button");
    button.innerHTML = "Start drawing";
    button.addEventListener("click", (e) => {
      e.preventDefault();
      map.addLayer(freeDraw);
      controls.parentNode.removeChild(controls);
    });
    controls.style.marginTop = "1em";
    controls.appendChild(
      document.createTextNode("Pan and zoom the map, then click: ")
    );
    controls.appendChild(button);
  }
  freeDraw.on("markers", (event) => {
    let geojson = {
      type: "MultiPolygon",
      coordinates: event.latLngs.map((shape) => [
        shape.map((p) => [p.lng, p.lat]),
      ]),
    };
    input.value = JSON.stringify(geojson);
  });
}
