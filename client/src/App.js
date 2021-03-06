import React, { useState, useEffect, useCallback } from 'react';
import './App.css'
import MySearchBar from './SearchBar';
import SearchResults from './SearchResults'

const port = process.env.PORT || 5000;

export default function App() {
  const [results,setResults] = useState([]);
  const [searchId, setSearchId] = useState("");
  const [stop,setStop] = useState(false);

  const parseMetaChars = inputStr => inputStr.replace(/"/g,'&quot;').replace(/\n/g,'&NewLine;').replace(/'/g,'&apos;')

  const getNewResults =useCallback(async id => {
    console.log("ask more results  for  si"+ id);
        const response = await fetch('http://localhost:'+port.toString()+'/api/getResults?si='+id, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json());

        console.log("response to results request os searcי id :"+id);
        console.log(response.data);
        setResults(response.data);
    },[setResults, results]);

  const getMoreResults =useCallback(async id => {
    console.log("ask more results  for  si"+ id);
        const response = await fetch('http://localhost:'+port.toString()+'/api/getResults?si='+id, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json());

        console.log("response to results request os searcי id :"+id);
        console.log(response.data);
        setResults(results.concat(response.data));
    },[setResults, results]);
  
  const getResultsOfSearch = newSearchId =>{
    setSearchId(newSearchId);
    if(!stop){
      getMoreResults();
      setStop(true);
    }
    
    };

  const handleSearch =useCallback( async searchTerm => {
     
        console.log("searching for "+ searchTerm);
        console.log(searchTerm);
        let query = parseMetaChars(searchTerm);
        console.log("parsed to "+ searchTerm);
        const response = await fetch('http://localhost:'+port.toString()+'/api/search?qu='+query, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json());
        // getResultsOfSearch(response.searchId);
        setSearchId(response.searchId);
        console.log("responseId "+response.searchId)
        getNewResults(response.searchId);
    },[setSearchId,getMoreResults, searchId]);

  const getMoreResultsNow = () => getMoreResults(searchId);

  return (
      
      <div className="App">
        <div className="appHeader">
        <h1>מנוע חיפוש הערות צד בחקיקה</h1>
        <h2>חלשים בגרפיקה, חזקים בהערות צד</h2>
        </div>
        <MySearchBar  handleClick={handleSearch} />
        <SearchResults results={results}/>
        <div className="moreResultsButton">
        <button  onClick={getMoreResultsNow}>קבל תוצאות נוספות</button>
        </div>
        
      </div>
  

  );
}
