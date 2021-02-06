import React, { useState, useEffect } from 'react';
import './App.css'
import MySearchBar from './SearchBar';
import SearchResults from './SearchResults'

const port = process.env.PORT || 5000;

export default function App() {
  const [results,setResults] = useState([]);
  const [searchId, setSearchId] = useState("");
  const [stop,setStop] = useState(false);

  const parseMetaChars = inputStr => inputStr.replace(/"/g,'&quot;').replace(/\n/g,'&NewLine;').replace(/'/g,'&apos;')

  const getMoreResults = async () => {
    console.log("ask more results  for  si"+ searchId);
        const response = await fetch('http://localhost:'+port.toString()+'/api/getResults?si='+searchId, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json());

        console.log("response to results request os searcי id :"+searchId);
        console.log(response.data);
        setResults(results.concat(response.data));
    };
  
  const getResultsOfSearch = newSearchId =>{
    setSearchId(newSearchId);
    if(!stop){
      getMoreResults();
      setStop(true);
    }
    
    };

  const handleSearch = async searchTerm => {
     
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
        getResultsOfSearch(response.searchId);
      
    };

  return (
      <div className="App">
        <MySearchBar  handleClick={handleSearch} />
        {/* <SearchResults results={results}/> */}
      </div>
  

  );
}
