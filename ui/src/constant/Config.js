export default {
    apiurl: process.env.NODE_ENV === "production"
        ? "https://api.craicbox.app"
        : "http://localhost:5001",
    isDebugMode: false
}
