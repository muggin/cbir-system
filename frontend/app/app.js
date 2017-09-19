import React from 'react';
import { connect } from 'react-redux'
import { Search, ImageCard } from './search'

const App = ({dispatch, images, base64File}) => (
  <div style={{ margin: '0 auto'}}>
    <div style={{display: 'flex', height: '400px', background: 'lightgrey'}}>
      <div style={{flex: '1 0 50%'}}>
        <Search />
      </div>
      <div style={{flex: '1 0 50%', textAlign: 'center'}}>
        <ImageCard image={base64File} />
      </div>
    </div>

    <div style={{display: 'flex', flexFlow: 'row wrap'}}>
      {images.map((image, i) => <ImageCard key={i} image={image} />)}
    </div>
  </div>
)

const mapStateToProps = (state) => ({
  images: state.search.images,
  base64File: state.search.base64File
})

export default connect(mapStateToProps)(App)
