import { useEffect } from 'react';
import './First.css';
import { useNavigate } from 'react-router-dom';
import { getSpeech } from '../util/GetSpeech';

function First() {
    const navigate = useNavigate();
    const touch = () => {
        fetch('http://127.0.0.1:5000/api/updown')
        .then(response => response.json());
        getSpeech('사용자의 키를 감지해 높이를 변경하는 중입니다. 잠시만 기다려주세요!')
        navigate('/wheretoeat');
    }

    useEffect(() => {
        window.speechSynthesis.getVoices();
    }, []);

    return (
        <>
            <div className='root'>
                <button className='touchButton' onClick={touch}>터치 후 메뉴를<br/>선택해주세요.</button>
            </div>
        </>
    );
}

export default First;