function getUser() {
    fetch("https://reqres.in/api/users/2", {
        headers: { "x-api-key": "pro_8a05f48f5e089a6ee6f70a879ff60a3d6fce85cfe3c426dbf2339fc827d24307" }
    })
        .then(response => {
            console.log("Status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Full response:", data);
        })
        .catch(error => {
            console.error("Network error:", error.message);
        })
        .finally(() => {
            console.log("Request finished.");
        });
}

getUser();