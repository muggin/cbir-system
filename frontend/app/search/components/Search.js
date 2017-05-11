import React, { Component } from 'react'
import { connect } from 'react-redux'
import { search, selectFeature, selectScoring } from '../actions'

const EVALUATIONS = [{value: 'cosine', text: 'Cosine'},
  {value: 'euclidean', text: 'Euclidean'},
  {value: 'chi2', text: 'Chi²'},
  {value: 'kl', text: 'K-L divergence'},
  {value: 'bhattacharyya', text: 'Bhattacharyya'},
  {value: 'intersection', text: 'Intersection'}]

const FEATURES = [{value: 'hist', text: 'Histograms'},
  {value: 'cnn', text: 'CNN'},
  {value: 'combination', text: 'CNN + Histograms'}]

const Search = ({dispatch, loading, feature}) => (
  <div style={{padding: '2em'}}>
    
    <label style={{fontSize: '1.6em', width: '70%', display: 'block', margin: '0 auto', textAlign: 'center', backgroundColor: loading ? 'grey' : 'turquoise', padding: '1em', borderRadius: '.5em', cursor: 'pointer', color: 'white'}}>
      Choose a file for image search
      <input type='file' name='file' id="file" style={{display: 'none'}} onClick={(e) => {
        if (!feature || !scoring) {
          alert('Please select a feature extractor and a scoring function')
          e.preventDefault()
          return
        }
      }} onChange={() => { 
        const files = document.getElementById('file').files
        const file = files[0]

        dispatch(search(file, feature))
      }} />
    </label> 
  
    <SelectionButtons title={'Choose feature extractor'} options={FEATURES} selectAction={(feature) => dispatch(selectFeature(feature))} />
    <SelectionButtons title={'Choose evaluation function'} options={EVALUATIONS} selectAction={(scoring) => dispatch(selectScoring(scoring))} />
  
  </div>
)

class SelectionButtons extends Component {
  constructor (props) {
    super(props)
    this.state = {selected: -1}
  }

  render () {
    const { options, selectAction, title } = this.props
    const { selected } = this.state
    return <div style={{marginTop: '15px', textAlign: 'center'}}>
      <section style={{fontSize: '1.2em'}}>{title}</section>
      { options.map((option, i) => 
      <div key={i} style={{backgroundColor: selected == i ? 'limegreen' : 'grey',
        display: 'inline-block',
        padding: '1em',
        color: 'white',
        borderRadius: '.5em',
        cursor: 'pointer',
        margin: '.2em'}}
        onClick={() => {
          this.setState({selected: i})
          selectAction(option.value)
        }}>
        {option.text}
      </div>) }
    </div>
  }
}

const mapStateToProps = (state) => ({
  loading: state.search.loading,
  feature: state.search.feature
})

export default connect(mapStateToProps)(Search)
