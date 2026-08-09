function getUser() {
    fetch("https://reqres.in/api/users/23", {
        headers: { "x-api-key": "pro_8a05f48f5e089a6ee6f70a879ff60a3d6fce85cfe3c426dbf2339fc827d24307" }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`User not found (status ${response.status})`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Full response:", data);
        })
        .catch(error => {
            console.error("Error:", error.message);
        })
        .finally(() => {
            console.log("Request finished.");
        });
}

getUser();