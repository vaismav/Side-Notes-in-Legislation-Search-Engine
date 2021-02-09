import React, { useState, useEffect } from 'react';


const side_note_str= "הערת צד : ";
const in_laws_str= "מופיע בחוקים : ";
const content_str= "תוכן : ";


function Results({side_note, law_names , html}){
    let laws_str = law_names.join(" , ");
    
    return(<div className="result">
        <h3>{side_note_str} {side_note}</h3>
        <h4>{in_laws_str} {laws_str}</h4>
        <h5>{content_str}</h5>
        {html}
    </div>);
}


export default function SearchResults({results}) {
    

    let render =  results.map(item => (<Results side_note={item._side_note} law_names={item.law_names} html={item.string_to_html}/>));

    return (<div className="searchResults"> {render}</div>);
}

