const summarize_btn = document.getElementById("summarize_btn");
const clear_btn = document.getElementById("clear_btn")

summarize_btn.addEventListener("click", async () => {
    let input_text = document.getElementById("input_text").value;
    const summary_text = document.getElementById("summary_text");
    summary_text.value = "Summarizing...";
    
    if(input_text.trim().length == 0){
        alert("please enter some text to summarize");
        document.getElementById("summary_text").value = "";
    }
    else{
        // async function send_request(){
            summarize_btn.disabled = true;
            try{
                const response = await fetch("/summarize", {
                    method : "POST",
                    headers : {
                        "Content-Type" : "application/json"
                    },
                    body : JSON.stringify({text : input_text})
                });
                const data = await response.json();
                
                summary_text.value = data.summary;

            }
            catch (error) {
                console.error("Error:", error);
                summary_text.value = "Something went wrong. Please try again.";
                summarize_btn.disabled = false;
            }
        }
    // }
    summarize_btn.disabled = false;
});

clear_btn.addEventListener("click", () => {
    document.getElementById("input_text").value = "";
    document.getElementById("summary_text").value = "";
});