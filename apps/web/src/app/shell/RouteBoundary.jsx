import React from 'react';

export default class RouteBoundary extends React.Component {
  state = {failed: false};
  static getDerivedStateFromError() {return {failed: true};}
  render() {
    if (this.state.failed) return <section className="empty-state" role="alert">
      <h2>This screen could not be opened</h2>
      <button className="secondary-button" onClick={() => this.setState({failed: false})}>Try again</button>
    </section>;
    return this.props.children;
  }
}
