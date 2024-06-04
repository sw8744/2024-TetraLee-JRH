import './Footer.css';

function Footer(children) {
    const previous = children.previous;
    const next = children.next;

    return (
        <footer className='footer2'>
            <button className='previousButton' onClick={previous}>이전</button>
            <button className='nextButton' onClick={next}>다음</button>
        </footer>
    );
}

export default Footer;