// ============================================================
// Mobile nav toggle
// ============================================================
const navToggle = document.getElementById("navToggle");
const tabs = document.querySelector(".tabbar__tabs");
if (navToggle && tabs) {
  navToggle.addEventListener("click", () => tabs.classList.toggle("is-open"));
}

// ============================================================
// Scroll-reveal: fade/slide elements in as they enter the viewport
// ============================================================
const revealEls = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && revealEls.length) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("is-visible"));
}

// ============================================================
// Terminal typing animation on the home page hero
// ============================================================
const typeTarget = document.getElementById("typeTarget");
const typeOut = document.getElementById("typeOut");
if (typeTarget) {
  const phrase = "whoami";
  let i = 0;
  const type = () => {
    if (i <= phrase.length) {
      typeTarget.textContent = phrase.slice(0, i);
      i++;
      setTimeout(type, 90);
    } else if (typeOut) {
      typeOut.hidden = false;
      typeOut.style.opacity = 0;
      typeOut.style.transition = "opacity 0.4s ease";
      requestAnimationFrame(() => (typeOut.style.opacity = 1));
    }
  };
  setTimeout(type, 400);
}

// ============================================================
// Live project search (projects page)
// Filters instantly on keystroke using the JSON embedded in the page;
// falls back to a normal form submit (server-rendered) if JS is off.
// ============================================================
const searchInput = document.getElementById("searchInput");
const projectList = document.getElementById("projectList");
const searchForm = document.getElementById("searchForm");
const searchStatus = document.getElementById("searchStatus");
const sitePrefix = document.querySelector('meta[name="site-prefix"]')?.content || "";

if (searchInput && projectList) {
  let allProjects = [];
  try {
    allProjects = JSON.parse(projectList.dataset.allProjects || "[]");
  } catch (e) {
    allProjects = [];
  }

  // Prevent full page reload; filter client-side instead.
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => e.preventDefault());
  }

  const escapeHtml = (str) =>
    str.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));

  const render = (projects, query) => {
    if (!projects.length) {
      projectList.innerHTML = `<p class="empty-state">No projects matched "${escapeHtml(query)}". Try a different word.</p>`;
      return;
    }
    projectList.innerHTML = projects
      .map(
        (p) => `
      <a class="commit is-visible" href="${sitePrefix}/projects/${p.slug}">
        <span class="commit__hash">${p.hash}</span>
        <span class="commit__msg">
          ${escapeHtml(p.title)}
          <span class="commit__summary">${escapeHtml(p.summary)}</span>
          <span class="tag-row">${p.tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join("")}</span>
        </span>
        <span class="commit__stat">
          <span class="stat-add">+${p.stats.additions}</span>
          <span class="stat-del">${p.stats.deletions}</span>
        </span>
      </a>`
      )
      .join("");
  };

  const filter = (query) => {
    const q = query.trim().toLowerCase();
    if (!q) return allProjects;
    return allProjects.filter((p) => {
      const haystack = [p.title, p.summary, p.description, ...p.tags, ...p.stack]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  };

  let debounceTimer;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const results = filter(e.target.value);
      render(results, e.target.value);
      if (searchStatus) {
        searchStatus.hidden = false;
        searchStatus.textContent = `${results.length} project${results.length === 1 ? "" : "s"} found`;
      }
      // Keep the URL shareable/bookmarkable without a full reload.
      const url = new URL(window.location);
      if (e.target.value) url.searchParams.set("q", e.target.value);
      else url.searchParams.delete("q");
      window.history.replaceState({}, "", url);
    }, 120);
  });
}

// ============================================================
// Screenshot lightbox (project detail page)
// ============================================================
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const lightboxClose = document.getElementById("lightboxClose");

document.querySelectorAll("[data-lightbox-src]").forEach((btn) => {
  btn.addEventListener("click", () => {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = btn.dataset.lightboxSrc;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  });
});

const closeLightbox = () => {
  if (!lightbox) return;
  lightbox.hidden = true;
  document.body.style.overflow = "";
};

if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
if (lightbox) {
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) closeLightbox();
  });
}
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeLightbox();
});
