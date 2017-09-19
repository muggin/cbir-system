import React from 'react'

const SearchBar = ({search}) => (
  <div>
    <input placeholder='Input your search here' style={{height: '40px', fontSize: '1.3em', width: '90%', padding: '.2em', margin: '0 auto', display: 'block'}} />
    SÖKBAR: {search}
  </div>
)

export default SearchBar
