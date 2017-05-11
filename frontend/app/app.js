import React from 'react';
import { connect } from 'react-redux'
import { Search, ImageCard } from './search'

const App = ({dispatch, images}) => (
  <div style={{ margin: '0 auto'}}>
    <Search />
    
    <div style={{display: 'flex', flexFlow: 'row wrap'}}>
      {images.map((image, i) => <ImageCard key={i} image={image} />)}
    </div>
  </div>
)

const mapStateToProps = (state) => ({
  images: state.search.images
})

export default connect(mapStateToProps)(App)
