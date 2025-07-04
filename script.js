document.getElementById("generate").addEventListener("click", async () => {
  const mood = document.getElementById("mood").value.trim();
  const output = document.getElementById("output");
  
  if (!mood) {
    output.innerHTML = `<p style="color:red;">Please enter how you are feeling.</p>`;
    return;
  }

  output.textContent = "Generating your motivational quote...";

  try {
    const response = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ mood })
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    const text = data.choices[0].message.content;
    output.innerHTML = `<p>${text}</p>`;
  } catch (err) {
    console.error(err);
    output.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});
