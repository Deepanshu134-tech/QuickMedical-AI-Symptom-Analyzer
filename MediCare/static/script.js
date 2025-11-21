document.getElementById('analyze-button').addEventListener('click', async function () {
    const symptoms = document.getElementById('symptom-input').value.trim();
    const resultsContainer = document.getElementById('results-container');

    // Clear previous results
    resultsContainer.innerHTML = "";
    resultsContainer.style.display = "block";

    // Check for empty input
    if (!symptoms) {
        alert("Please enter your symptoms before analyzing.");
        return;
    }

    // Show loading spinner
    const spinner = document.createElement("div");
    spinner.id = "loading-spinner";
    spinner.classList.add("show-spinner");
    resultsContainer.appendChild(spinner);

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms })
        });

        if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
        const analysis = await response.json();

        // Remove spinner
        spinner.remove();

        if (analysis.error) {
            const errorMsg = document.createElement("p");
            errorMsg.textContent = `Error: ${analysis.error}`;
            resultsContainer.appendChild(errorMsg);
            return;
        }

        // Helper to create list section
        function createListSection(titleText, items) {
            const section = document.createElement("section");
            section.classList.add("result-section", "result-fade-in");

            const title = document.createElement("h2");
            title.textContent = titleText;
            section.appendChild(title);

            const list = document.createElement("ul");
            items.forEach(item => {
                const li = document.createElement("li");
                if (typeof item === "object" && item.name && item.probability) {
                    const strong = document.createElement("strong");
                    strong.textContent = item.name;
                    li.appendChild(strong);
                    li.appendChild(document.createTextNode(` (Probability: ${item.probability})`));
                } else {
                    li.textContent = item;
                }
                list.appendChild(li);
            });

            section.appendChild(list);
            resultsContainer.appendChild(section);
        }

        // Helper to create urgency section
        function createUrgencySection(urgency) {
            const section = document.createElement("section");
            section.classList.add("result-section", "result-fade-in");

            const title = document.createElement("h2");
            title.textContent = "Urgency Level (1-5 Scale)";
            section.appendChild(title);

            const urgencyDisplay = document.createElement("div");
            urgencyDisplay.id = "urgency-level-display";
            urgencyDisplay.textContent = `${urgency} / 5`;
            urgencyDisplay.style.backgroundColor =
                urgency >= 4 ? 'var(--urgency-high)' :
                urgency === 3 ? 'var(--urgency-medium)' :
                'var(--urgency-low)';
            section.appendChild(urgencyDisplay);

            resultsContainer.appendChild(section);
        }

        // Render all sections dynamically
        createListSection("Possible Conditions", analysis.conditions);
        createUrgencySection(analysis.urgency);
        createListSection("Immediate Actions", analysis.actions);
        createListSection("When to See a Doctor", analysis.triggers);
        createListSection("Questions for Doctor", analysis.questions);

    } catch (error) {
        console.error("Fetch Error:", error);
        spinner.remove();
        const errorMsg = document.createElement("p");
        errorMsg.textContent = "Could not connect to the analysis service. Please ensure the Python server is running and try again.";
        resultsContainer.appendChild(errorMsg);
    }
});
