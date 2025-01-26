async function transliterate() {
    const inputText = document.getElementById('inputText').value;
    const transliterationType = document.getElementById('transliterationType').value;

    const response = await fetch('http://127.0.0.1:5000/transliterate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText, type: transliterationType })
    });

    const result = await response.json();
    document.getElementById('outputText').innerText = result.transliterated_text;
}

window.onload = function() {
    let textarea = document.getElementById('inputText');
    let placeholders = ["enter text / baravun pADle...", "ಎಂಟೆರ್ ತೆಕ್ಸ್ತ್ / ಬರವುನ್ ಪಾಡ್ಲೆ..."];
    let index = 0;

    // Function to cycle placeholder text
    function changePlaceholder() {
        textarea.placeholder = placeholders[index];
        index = (index + 1) % placeholders.length; // Cycle between 0 and 1
    }

    // Change placeholder every how many seconds
    setInterval(changePlaceholder, 2000);
};

document.addEventListener("DOMContentLoaded", () => {
    const textElement = document.getElementById("outputText");
    textElement.innerHTML = textElement.innerHTML.replace(/J/g, '<span class="special">J</span>');
  });