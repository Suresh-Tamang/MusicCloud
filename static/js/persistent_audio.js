class AudioPlayer {
  constructor() {
    this.audio = document.getElementById("audio-player");
    this.currentTitle = document.getElementById("current-song-title");
    this.currentArtist = document.getElementById("current-song-artist");

    // Restore state when page loads
    this.loadState();

    // Save state periodically
    setInterval(() => this.saveState(), 1000);

    // Save state before page unloads
    window.addEventListener("beforeunload", () => this.saveState());

    // Handle play buttons (no link prevention)
    document.body.addEventListener("click", (e) => {
      const playBtn = e.target.closest(".play-btn");
      if (playBtn) this.handlePlayButton(playBtn);
    });
  }

  loadState() {
    const state = JSON.parse(localStorage.getItem("audioState") || "{}");
    if (state.src) {
      this.audio.src = state.src;
      this.audio.currentTime = state.time || 0;
      this.currentTitle.textContent = state.title || "";
      this.currentArtist.textContent = state.artist || "";

      if (state.playing) {
        // Handle autoplay restrictions
        this.audio.play().catch((e) => console.log("Autoplay blocked:", e));
      }
    }
  }

  saveState() {
    localStorage.setItem(
      "audioState",
      JSON.stringify({
        src: this.audio.src,
        time: this.audio.currentTime,
        playing: !this.audio.paused,
        title: this.currentTitle.textContent,
        artist: this.currentArtist.textContent,
      })
    );
  }

  handlePlayButton(btn) {
    const songCard = btn.closest(".song-card");
    this.playSong(
      songCard.dataset.audioUrl,
      songCard.querySelector("h3").textContent,
      songCard.querySelector(".song-info p").textContent
    );
  }

  playSong(url, title, artist) {
    this.audio.src = url;
    this.currentTitle.textContent = title;
    this.currentArtist.textContent = artist;

    this.audio
      .play()
      .then(() => this.updateUI())
      .catch((e) => console.log("Playback error:", e));

    this.saveState();
  }

  updateUI() {
    document.querySelectorAll(".song-card").forEach((card) => {
      const isCurrent = card.dataset.audioUrl === this.audio.src;
      card.classList.toggle("currently-playing", isCurrent);

      if (isCurrent) {
        const btn = card.querySelector(".play-btn i");
        btn?.classList.replace("fa-play", "fa-pause");
      }
    });
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.audioPlayer = new AudioPlayer();
});
