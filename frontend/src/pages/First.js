import './First.css';
import { useNavigate } from 'react-router-dom';

function First() {
    const navigate = useNavigate();
    const touch = () => {
        fetch('http://127.0.0.1:5000/api/updown')
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