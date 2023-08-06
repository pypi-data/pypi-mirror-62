export async function render() {
  const origin = document.location.origin;
  const tfTensorboard = window.parent.document.querySelector('tf-tensorboard');
  const iFrame = tfTensorboard.shadowRoot.querySelector(
      'div[data-dashboard="profile"] > iframe');
  iFrame.reload = () => {
    iFrame.src = origin + '/data/plugin/profile/index.html';
  };
  document.location.href = 'index.html';
}
