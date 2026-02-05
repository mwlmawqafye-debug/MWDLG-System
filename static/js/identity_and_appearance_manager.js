
document.addEventListener('DOMContentLoaded', () => {
    const colorMatrixRadios = document.querySelectorAll('input[name="color_matrix"]');
    const systemFontSelect = document.getElementById('system-font');
    const frappeModeToggle = document.getElementById('frappe-mode');
    const subtlePatternToggle = document.getElementById('subtle-pattern');
    const saveButton = document.querySelector('.save-button');

    // --- Live Preview Logic ---

    // 1. Color Theme
    const applyColorTheme = (theme) => {
        const root = document.documentElement;
        // Define themes based on the value of the radio buttons
        const themes = {
            'waqf': { '--waqf-green': '#1b4d3e', '--background-color': '#f8f9fa', '--text-color': '#212529' },
            'manuscript': { '--waqf-green': '#8b4513', '--background-color': '#f5f5dc', '--text-color': '#5b3a1a' },
            'hybrid': { '--waqf-green': '#1b4d3e', '--background-color': '#f5f5dc', '--text-color': '#212529' },
            'sovereign': { '--waqf-green': '#003366', '--background-color': '#f8f9fa', '--text-color': '#212529' },
        };
        
        const selectedTheme = themes[theme];
        if (selectedTheme) {
            for (const [key, value] of Object.entries(selectedTheme)) {
                root.style.setProperty(key, value);
            }
        }
    };

    colorMatrixRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            applyColorTheme(e.target.value);
        });
    });

    // 2. Font Selection
    systemFontSelect.addEventListener('change', (e) => {
        document.body.style.fontFamily = `'${e.target.value}', sans-serif`;
    });

    // --- Save Logic ---
    saveButton.addEventListener('click', async () => {
        const settings = {
            color_matrix_selection: document.querySelector('input[name="color_matrix"]:checked').value,
            enable_frappe_mode: frappeModeToggle.checked,
            system_font: systemFontSelect.value,
            enable_subtle_pattern: subtlePatternToggle.checked,
            system_title: document.getElementById('system-title').value
        };

        console.log("Saving settings:", settings);
        saveButton.textContent = '💾 جاري الحفظ...';
        saveButton.disabled = true;

        try {
            // The API endpoint '/api/identity_settings' will be created in the next phase.
            const response = await fetch('/api/identity_settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Save successful:", result);
            alert('تم حفظ الإعدادات بنجاح!'); // Simple feedback
        
        } catch (error) {
            console.error("Error saving settings:", error);
            alert('حدث خطأ أثناء حفظ الإعدادات. يرجى مراجعة وحدة التحكم.');
        } finally {
            saveButton.textContent = '💾 تثبيت التغييرات';
            saveButton.disabled = false;
        }
    });

    // Apply initial theme on load
    const initialTheme = document.querySelector('input[name="color_matrix"]:checked').value;
    applyColorTheme(initialTheme);
000});
