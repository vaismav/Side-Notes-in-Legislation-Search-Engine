import React, { useState, useEffect, useCallback } from 'react';
// import { SearchBar } from 'react-native-elements';

const port = process.env.PORT || 5000;
console.log("port: " + port);


export default function MySearchBar({ handleClick}) {
    const [suggestions,setSugestions] = useState([]);
    const [suggestElement,setSuggestElement] = useState([]);
    const [searchTerm, setSearchTerm] = useState("")

    const setAndUpdateSuggestions =(data) =>{
        setSugestions(data);
        setSuggestElement(data.map(value => (<dt>{value}</dt>)));
    }
    
    const handleChange = useCallback(
        async event => {
            setSearchTerm(event.target.value);
            console.log("event.target.value = "+event.target.value)
            console.log("input = "+searchTerm)
            if(event.target.value != ""){
                event.preventDefault();
                const response = await fetch('http://localhost:'+port.toString()+'/api/searchOption?qu='+event.target.value, {
                    method: 'GET',
                    headers: {
                    'Content-Type': 'application/json'
                    }
                }).then(res => res.json());
                setAndUpdateSuggestions(response.data);
            }
        },
        [setSearchTerm,searchTerm]
      );
     
    const fillSearchInput = choice => {
        setSearchTerm(choice);
    }    
   
    const createSuggestionList = () => (<div className="flatList">{suggestions.map(value => (<div className="suggestItem" ><p >{value}</p></div>))}</div>);
    // onClick={fillSearchInput(value)}
    
    const handleFocus = () => setSuggestElement([createSuggestionList()]); 

    const handleBlur = () => setSuggestElement([]); 
    
    const onClickHandle = useCallback(event => handleClick(searchTerm),[searchTerm]);
    
    return ( 
            <div className="SearchBar">
              <div>
              <button onClick={onClickHandle} >חפש</button>
                <input
                type="text"
                id="field"
                value={searchTerm}
                onChange={handleChange}
                onFocus={handleFocus}
                onBlur={handleBlur}
                placeholder="הקלד הערת צד לחיפוש"></input>
                
                </div>
                <div>{suggestElement}</div>
            </div>
        );
    
}