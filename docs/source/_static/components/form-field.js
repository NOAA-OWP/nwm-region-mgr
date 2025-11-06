class FormField extends HTMLElement {
  connectedCallback() {
    const label = this.getAttribute("label") || "Label";
    const tooltip = this.getAttribute("tooltip") || "";
    const name = this.getAttribute("name") || "";
    const type = this.getAttribute("type") || "text"; // "text", "select", "checkbox"
    const placeholder = this.getAttribute("placeholder") || "";
    const required = this.hasAttribute("required");
    const yamlPath = this.getAttribute("data-yaml") || "";
    const options = this.getAttribute("options"); // for select
    const multiple = this.hasAttribute("multiple");
    const defaultValue = this.getAttribute("data-default") || "";

    let inputHTML;

    if (type === "select") {
        const opts = options
            ? options.split(",").map(o => `<option value="${o.trim()}">${o.trim()}</option>`).join("")
            : "";
        inputHTML = `<select id="${name}" name="${name}" data-yaml="${yamlPath}" ${required ? "required" : ""} ${multiple ? "multiple" : ""}>
                        ${!multiple ? `<option value="">-- Select --</option>` : ""}
                        ${opts}
                    </select>`;

        // Set the default after DOM insertion
        setTimeout(() => {
            const sel = this.querySelector("select");
            if (!sel) return;
            if (multiple) {
            const values = (defaultValue || "").split(",").map(v => v.trim());
            Array.from(sel.options).forEach(o => { o.selected = values.includes(o.value); });
            } else if (defaultValue) {
            sel.value = defaultValue;
            }
        }, 0);

    } else if (type === "checkbox") {
      inputHTML = `<input type="checkbox" id="${name}" name="${name}" data-yaml="${yamlPath}" ${defaultValue === "true" ? "checked" : ""}>`;

    } else {
      inputHTML = `<input id="${name}" name="${name}" type="${type}" placeholder="${placeholder}" data-yaml="${yamlPath}" ${required ? "required" : ""} value="${defaultValue}"/>`;
    }

    this.innerHTML = `
      <div class="form-field">
        <label for="${name}">
          ${label}
          ${tooltip ? `<span data-tippy-content="${tooltip}">
                        <button type="button" class="icon-btn" aria-label="${label} help">i</button>
                      </span>` : ""}
        </label>
        ${inputHTML}
      </div>
    `;
  }
}

customElements.define("form-field", FormField);
