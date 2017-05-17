/* global fetch */
export const SEARCH_LOADING = 'SEARCH_LOADING'
export const SEARCH_SUCCESS = 'SEARCH_SUCCESS'
export const SEARCH_ERROR = 'SEARCH_ERROR'

export const search = (file, feature, evaluation) => {
  return dispatch => {
    dispatch({type: SEARCH_LOADING})

    const reader = new FileReader()

    reader.readAsDataURL(file)

    const fileName = file.name
    const fileEnding = fileName.substring(fileName.length - 3, fileName.length)
    
    reader.addEventListener("load", function () {
      return fetch('http://localhost:8081/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({image: reader.result, file_ending: fileEnding, feature, evaluation})
      })
      .then(response => response.json())
      //.then(dict => dict.hits.hits.map(img => img._source['doc_name']))
      .then(({images, data_path}) => images.map(img => data_path + img))
      .then(images => {
        dispatch({type: SEARCH_SUCCESS, images})
      })
      .catch(error => dispatch({type: SEARCH_ERROR, error}))
    }, false);


  }
}

export const SELECT_FEATURE = 'SELECT_FEATURE'

export const selectFeature = feature => ({type: SELECT_FEATURE, feature})

export const SELECT_EVALUATION = 'SELECT_EVALUATION'

export const selectEvaluation = evaluation => ({type: SELECT_EVALUATION, evaluation})
