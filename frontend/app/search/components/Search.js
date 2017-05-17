import React, { Component } from 'react'
import { connect } from 'react-redux'
import { search, selectFeature, selectEvaluation, base64File } from '../actions'

const EVALUATIONS = [{value: 'cosine', text: 'Cosine'},
  {value: 'euclidean', text: 'Euclidean'},
  {value: 'chi2', text: 'Chi²'},
  {value: 'kl', text: 'K-L divergence'},
  {value: 'bhattacharyya', text: 'Bhattacharyya'},
  {value: 'intersection', text: 'Intersection'}]

const FEATURES = [{value: 'hist_basic', text: 'Histograms'},
  {value: 'cnn_basic', text: 'CNN'},
  {value: 'cnn_hist', text: 'CNN + Histograms'}]

const Search = ({dispatch, loading, feature, evaluation}) => (
  <div style={{padding: '2em'}}>
    
    <label style={{fontSize: '1.6em', width: '70%', display: 'block', margin: '0 auto', textAlign: 'center', backgroundColor: loading ? 'grey' : 'turquoise', padding: '1em', borderRadius: '.5em', cursor: 'pointer', color: 'white'}}>
      Choose a file for image search
      <input type='file' name='file' id="file" style={{display: 'none'}} onClick={(e) => {
        if (!feature || !evaluation) {
          alert('Please select a feature extractor and a evaluation function')
          e.preventDefault()
          return
        }
      }} onChange={() => { 
        const files = document.getElementById('file').files
        if (files.length == 0) return
        const file = files[0]

        dispatch(search(file, feature, evaluation))
      }} />
    </label> 
  
    <SelectionButtons title={'Choose feature extractor'} options={FEATURES} selectAction={(feature) => dispatch(selectFeature(feature))} />
    <SelectionButtons title={'Choose evaluation function'} options={EVALUATIONS} selectAction={(evaluation) => dispatch(selectEvaluation(evaluation))} />
  
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
  feature: state.search.feature,
  evaluation: state.search.evaluation
})

export default connect(mapStateToProps)(Search)
