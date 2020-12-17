import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        step: null,
    },
    mutations: {
        setStep(state, step) {
            state.step = step;
        }
    },
    actions: {}
});