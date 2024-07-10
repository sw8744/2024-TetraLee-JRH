import './First.css';
import { useNavigate } from 'react-router-dom';
import getSpeech from '../util/GetSpeech';

function First() {
    const navigate = useNavigate();
    function wait(sec) {
        let start = Date.now(), now = start;
        while (now - start < sec * 1000) {
            now = Date.now();
        }
    }
     const touch = async () => {
        await getSpeech('키에 맞춰 높이를 조절 중입니다! 화면이 멈추면 진행해주세요.');
        wait(5.5);
        await fetch('http://127.0.0.1:5000/api/updown')
        .then(response => response.json());
        navigate('/wheretoeat');
    }
    return (
        <>
            <div className='root'>
                <button className='touchButton' onClick={touch}>터치 후 메뉴를<br/>선택해주세요.</button>
            </div>
        </>
    );
}

export default First;