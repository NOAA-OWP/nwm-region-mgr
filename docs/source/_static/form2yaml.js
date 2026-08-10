(function () {
  // Utility: deep set into nested object
  function setDeep(obj, path, value) {
    const keys = path.split(".");
    let curr = obj;
    for (let i = 0; i < keys.length - 1; i++) {
      if (!curr[keys[i]]) curr[keys[i]] = {};
      curr = curr[keys[i]];
    }
    curr[keys[keys.length - 1]] = value;
  }

  function collectData(form) {
    const data = {};
    form.querySelectorAll("[data-yaml]").forEach(el => {
        const path = el.dataset.yaml;

        // Handle checkbox groups
        if (el.tagName.toLowerCase() === "div" && el.classList.contains("checkbox-group")) {
        const checked = Array.from(el.querySelectorAll("input[type=checkbox]:checked"))
            .map(cb => cb.value);
        setDeep(data, path, checked);

        // Handle <select> dropdowns
        } else if (el.tagName.toLowerCase() === "select") {
        if (el.multiple) {
            // multiple select → array of selected values
            const selected = Array.from(el.selectedOptions).map(opt => opt.value);
            setDeep(data, path, selected);
        } else {
            // single select
            setDeep(data, path, el.value);
        }
        // Handle check boxes
        } else if (el.type === "checkbox") {
            setDeep(data, path, el.checked);
        // Handle everything else (text, number, etc.)
        } else if (el.type !== "checkbox") {
        setDeep(data, path, el.value);
        }
    });
    return data;
    }

  function needsQuotes(str) {
    return /[:\-\[\]\{\},&\*#\?\|<>=\!%@`]|^\s|\s$|\n/.test(str);
  }
  function escYAML(val) {
    if (val === null || val === undefined) return '""';
    const s = String(val);
    return needsQuotes(s) ? JSON.stringify(s) : s;
  }

  function toYAML(obj, indent = "") {
    let out = "";
    for (const [k, v] of Object.entries(obj)) {
      if (Array.isArray(v)) {
        if (v.length === 0) {
          out += indent + k + ": []\n";
        } else {
          out += indent + k + ":\n";
          v.forEach(item => { out += indent + "  - " + escYAML(item) + "\n"; });
        }
      } else if (typeof v === "object" && v !== null) {
        out += indent + k + ":\n" + toYAML(v, indent + "  ");
      } else {
        out += indent + k + ": " + escYAML(v) + "\n";
      }
    }
    return out;
  }

  function download(filename, text, mime = "text/yaml") {
    const blob = new Blob([text], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // Attach to any form with .yaml-export-form
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("form.yaml-export-form").forEach(form => {
      const btn = form.querySelector(".download-yaml");
      if (!btn) return;
      btn.addEventListener("click", () => {
        if (!form.reportValidity()) return;
        const data = collectData(form);
        const yaml = toYAML(data);
        const fileBase = form.getAttribute("data-filename") || "form";
        download(fileBase + ".yaml", yaml);
      });
    });
  });
})();

// Fill in defaults
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".fill-defaults").forEach(btn => {
    btn.addEventListener("click", () => {
      const form = btn.closest("form");
      if (!form) return;

      // Standard inputs/selects
      form.querySelectorAll("input, select, textarea").forEach(el => {
        const defaultValue = el.dataset.default || el.placeholder || "";
        if (!defaultValue) return;

        if (el.tagName.toLowerCase() === "select") {
          if (el.multiple) {
            const values = defaultValue.split(",").map(v => v.trim());
            Array.from(el.options).forEach(opt => {
              opt.selected = values.includes(opt.value);
            });
          } else {
            el.value = defaultValue;
          }
        } else {
          el.value = defaultValue;
        }
      });

      // Shadow DOM inputs inside <form-field>
      form.querySelectorAll("form-field").forEach(ff => {
        const shadowInput = ff.shadowRoot?.querySelector("input, select, textarea");
        if (!shadowInput) return;
        const defaultValue = shadowInput.dataset.default || shadowInput.placeholder || "";
        if (!defaultValue) return;

        if (shadowInput.tagName.toLowerCase() === "select") {
          if (shadowInput.multiple) {
            const values = defaultValue.split(",").map(v => v.trim());
            Array.from(shadowInput.options).forEach(opt => {
              opt.selected = values.includes(opt.value);
            });
          } else {
            shadowInput.value = defaultValue;
          }
        } else {
          shadowInput.value = defaultValue;
        }
      });
    });
  });
});

