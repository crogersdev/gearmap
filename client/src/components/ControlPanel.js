import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import classes from './ControlPanel.module.css';

const mapStateToProps = (state) => ({
    mapInfo: state.mapUpdateReducer.mapInfo,
    observationData: state.mapUpdateReducer.observationData,
});

class ControlPanel extends Component {
    constructor(props) {
        super(props);
        this.state = { searchValue: 'Search...',
                       mapInfo: props.mapInfo };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleNewObservation = this.handleNewObservation.bind(this);
    }

    handleChange = (event) => {
        //console.log(event.target.value);
        this.setState({
            ...this.state,
            searchValue: event.target.value
        });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        this.props.applyFilters(this.state);
    }

    handleNewObservation = (event) => {
        console.log('new observation');
        

    }

    shouldComponentUpdate(nextProps, nextState) {
        return (this.props === nextProps ? false : true);
    }

    componentDidUpdate() {
        this.setState(this.props);
    }

    render() {
        return (
            <div className={classes.ControlPanel}>
                <form>
                    <input type="text"
                        /*defaultValue={this.state.searchValue}*/
                        placeholder="Search..."
                        onChange={ (target) => this.handleChange(target) }/>
                    <button 
                        onClick={ (target) => this.handleSubmit(target) }>Search</button>
                </form>
                <button
                    onClick={ (target) => this.handleNewObservation(target) }>
                    New Observation
                </button>
            </div>
        )
    }
}
export default connect(
    mapStateToProps,
)(ControlPanel);

ControlPanel.propTypes = {
    updateMapInfo: PropTypes.func.isRequired,
    applyFilters: PropTypes.func.isRequired,
}
