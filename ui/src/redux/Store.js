// src/js/store/index.js
import { createStore } from "redux";
import rootReducer from "./RootReducer";

const store = createStore(rootReducer);
export default store;