/**
* Calls an API endpoint, handling errors
* - Converts non-200 statuses into errors
* - Adds context to errors
*/
export const handleRequest = async (method, url, failureMessage) => {
  try {
    console.log(`${method} ${url}`);
    const res = await fetch(url, { method });
    
    var resBody = await res.json();
    
    if (res.status !== 200) {
      const errorText = resBody.message || resBody.error || "Error Unknown";
      const error = new Error(`${errorText} (Error: ${res.status})`);
      throw error;
    }
    return resBody;
  } catch (err) {
    const error = new Error(`${failureMessage}. ${err.message}`);
    throw error;
  }
};