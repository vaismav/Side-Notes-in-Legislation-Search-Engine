import React, { useState, useEffect } from 'react';
import XMLViewer from 'react-xml-viewer'
import  parse from 'html-react-parser' 

const side_note_str= "הערת צד : ";
const in_laws_str= "מופיע בחוקים : ";
const content_str= "תוכן : ";




function Results({side_note, law_names , html}){
    // let laws_str = law_names.join(" , ");
    let laws_str = law_names.map(name => (<p>{name}</p>));
    return(<div className="result">
        
       {/* <div className="resultContent">{parse(html)}</div> */}
        <div className="resultMeta">
        <h3>{side_note_str}</h3>
        <h3>{side_note}</h3>
        <h4>{in_laws_str}</h4>
        <h4>{laws_str}</h4>
        </div>
        {parse('<div className="resultContent">'+html+'</div>')}
        
        
        {/* <XMLViewer xml={html} /> */}
    </div>);
}


export default function SearchResults({results}) {
    

    let render =  results.map(item => (<Results side_note={item._side_note} law_names={item.law_names} html={item.string_to_html}/>));

    return (<div className="searchResults"> {render}</div>);
}

