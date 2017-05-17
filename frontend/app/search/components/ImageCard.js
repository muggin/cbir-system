import React from 'react'

const ImageCard = ({image}) => (
  <div style={{flex: '1 0 15em', position: 'relative', margin: '.3em'}}>
    <img style={{width: '100%', height: '360px', width: 'auto'}} src={image}/>
  </div>
)

export default ImageCard
