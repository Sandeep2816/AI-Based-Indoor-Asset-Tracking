const socket = io();
const assets = new Map();
const statusEl = document.getElementById("status");
const mapEl = document.getElementById("map");
const listEl = document.getElementById("assets");

socket.on("connect", () => { statusEl.textContent = "Live"; });
socket.on("disconnect", () => { statusEl.textContent = "Disconnected"; });

socket.on("asset_update", asset => {
  assets.set(asset.tag_id, asset);
  render();
});

async function loadInitial() {
  const response = await fetch("/api/assets");
  const data = await response.json();
  data.forEach(asset => assets.set(asset.tag_id, asset));
  render();
}

function render() {
  document.querySelectorAll(".asset-marker, .asset-label").forEach(el => el.remove());
  listEl.innerHTML = "";

  for (const asset of assets.values()) {
    const x = Math.max(2, Math.min(98, asset.position.x * 10));
    const y = Math.max(2, Math.min(98, 100 - asset.position.y * 12.5));

    const marker = document.createElement("div");
    marker.className = "asset-marker";
    marker.style.left = x + "%";
    marker.style.top = y + "%";

    const label = document.createElement("div");
    label.className = "asset-label";
    label.style.left = x + "%";
    label.style.top = y + "%";
    label.textContent = asset.tag_id;

    mapEl.append(marker, label);

    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML =
      "<strong>" + asset.tag_id + "</strong>" +
      "Position: (" + asset.position.x + " m, " + asset.position.y + " m)<br>" +
      "Anchors reporting: " + Object.keys(asset.anchors).length;
    listEl.appendChild(card);
  }
}

loadInitial();
