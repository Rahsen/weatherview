import React from 'react';

class Basic extends React.Component {
    constructor(props) {
        super(props);
        this.value = (new Date()).toLocaleDateString()
    }

    render() {
        return (
          <p>
              {this.value}
          </p>
        );
    }
}

export default Basic
