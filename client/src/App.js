import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';

const port = process.env.PORT || 5000;

export default function App() {
  const [results,setResults] = useState([]);

  const parseMetaChars = inputStr => inputStr.replace(/"/g,'&quot;').replace(/\n/g,'&NewLine;').replace(/'/g,'&apos;')

  const handleSearch = async searchTerm => {
    console.log("searching for "+ searchTerm);
        let query = parseMetaChars(searchTerm);
        console.log("parsed to "+ searchTerm);
        const response = await fetch('http://localhost:'+port.toString()+'/api/search?qu='+query, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json());
        setResults(response.data);
    };

  return (
    
      <div className="App">
        <SearchBar  handleClick={handleSearch} />
      </div>
    
  );
}
