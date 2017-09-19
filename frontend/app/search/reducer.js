import { combineReducers } from 'redux'
import * as actions from './actions'

const images = (state = [], {type, images}) => {
  switch (type) {
    case actions.SEARCH_SUCCESS: return images
    default: return state
  }
}

const loading = (state = false, {type}) => {
  switch (type) {
    case actions.SEARCH_LOADING: return true
    case actions.SEARCH_ERROR:
    case actions.SEARCH_SUCCESS: return false
    default: return state
  }
}

const feature = (state = null, {type, feature}) => {
  switch (type) {
    case actions.SELECT_FEATURE: return feature
    default: return state
  }
}

const evaluation = (state = null, {type, evaluation}) => {
  switch (type) {
    case actions.SELECT_EVALUATION: return evaluation
    default: return state
  }
}

const base64File = (state = null, {type, file}) => {
  switch (type) {
    case actions.BASE_64_FILE: return file
    default: return state
  }
}

export default combineReducers({
  images,
  loading,
  feature,
  evaluation,
  base64File
})
