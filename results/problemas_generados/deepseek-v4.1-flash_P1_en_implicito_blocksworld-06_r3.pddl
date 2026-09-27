(define (problem blocksworld-six)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (handempty)
    (clear f)
    (clear d)
    (ontable b)
    (ontable c)
    (on e b)
    (on f e)
    (on a c)
    (on d a)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
