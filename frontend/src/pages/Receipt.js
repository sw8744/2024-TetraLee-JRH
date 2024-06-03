import './Receipt.css';
import { useState } from 'react';

function Receipt() {
    const [number, setNumber] = useState(0);

    return (
        <>
            <header className='header'></header>
            <div>
                <p className='oct'>결제가 완료되었습니다.<br/></p>
                <p className='make'>영수증을</p>
                <p className='make'>출력하시겠습니까?</p>
            </div>
            <div className='coke'>
                <button className='yesButton'>예</button>
                <button className='noButton'>아니오</button>
            </div>
            <div className='bread'>
                <button className='react'>주문 번호 {number}번</button>
            </div>
        </>
    );
}

export default Receipt;