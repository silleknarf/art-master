import React from "react";
import { storiesOf } from "@storybook/react";
import * as FetchMock from "fetch-mock";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap-theme.css";
import Review from "../components/common/Review";

const createEntry = (entryId, entryKey, entryValue) => { 
  return { entryId, entryComponents: [ { key: entryKey, value: entryValue } ]};
};

storiesOf("Review", module)
  .add("with images", () => {
    FetchMock.restore()
    const ratings = [
      { userId: 1, imageBase64: "1/1.png", username: "User1", votes: 1},
      { userId: 2, imageBase64: "1/1.png", username: "User2", votes: 2}
    ];
    FetchMock.get("glob:*ratings?*", ratings);
    return <Review roundId="97" />;
  })
  .add("with words", () => {
    FetchMock.restore()
    const ratings = [
      { userId: 1, username: "User1", entry: createEntry(1, "Word", "test word"), votes: 1},
      { userId: 2, username: "User2", entry: createEntry(2, "Word", "test word 2"), votes: 2}
    ];
    FetchMock.get("glob:*ratings?*", ratings);
    return <Review roundId="97" />;
  })
  .add("with sentence", () => {
    FetchMock.restore()
    const ratings = [
      { userId: 1, username: "User1", entry: createEntry(1, "Sentence", "test sentence"), votes: 1},
      { userId: 2, username: "User2", entry: createEntry(2, "Sentence", "test sentence 2"), votes: 2}
    ];
    FetchMock.get("glob:*ratings?*", ratings);
    return <Review roundId="97" />;
  });