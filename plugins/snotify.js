import Vue from 'vue'
import 'vue-snotify/styles/material.css'
import Snotify, { SnotifyPosition } from 'vue-snotify'

const options = {
  toast: {
    position: SnotifyPosition.rightTop,
    timeout: 500
  }
}

Vue.use(Snotify, options)
